# Гибкий скрипт для создания симлинков схем
param(
    [string]$RepoPath = ".",  # Относительный путь к репозиторию
    [string]$SchemaVersion = "v1.9"  # Версия схемы для симлинков
)

Write-Host "🔗 Creating symlinks for schemas version $SchemaVersion..." -ForegroundColor Green

# Получаем абсолютный путь к репозиторию
$repoAbsolutePath = (Get-Item $RepoPath).FullName
$schemasPath = Join-Path $repoAbsolutePath "schemas"

if (-not (Test-Path $schemasPath)) {
    Write-Host "❌ Error: schemas directory not found at $schemasPath" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Repository path: $repoAbsolutePath" -ForegroundColor Gray
Write-Host "📁 Schemas path: $schemasPath" -ForegroundColor Gray

# Типы схем для обработки
$schemaTypes = @(
    "deepseek-instructions",
    "context-config",
    "selective-export", 
    "return-export"
)

$successCount = 0
$errorCount = 0
$skippedCount = 0

foreach ($schemaType in $schemaTypes) {
    $schemaDir = Join-Path $schemasPath $schemaType
    
    if (-not (Test-Path $schemaDir)) {
        Write-Host "⚠️  Skipping: Directory '$schemaType' not found" -ForegroundColor Yellow
        $skippedCount++
        continue
    }

    $targetFile = "$SchemaVersion.schema.json"
    $targetPath = Join-Path $schemaDir $targetFile
    $symlinkPath = Join-Path $schemaDir "latest.schema.json"

    if (-not (Test-Path $targetPath)) {
        Write-Host "⚠️  Skipping: Target file '$targetFile' not found in '$schemaType'" -ForegroundColor Yellow
        $skippedCount++
        continue
    }

    # Удаляем старый симлинк если существует
    if (Test-Path $symlinkPath) {
        try {
            Remove-Item $symlinkPath -Force -ErrorAction Stop
            Write-Host "🗑️  Removed old symlink: $schemaType/latest.schema.json" -ForegroundColor Gray
        }
        catch {
            Write-Host "❌ Error removing old symlink for $schemaType : $($_.Exception.Message)" -ForegroundColor Red
            $errorCount++
            continue
        }
    }

    # Создаем новый симлинк
    try {
        # Используем относительный путь для симлинка
        $relativeTargetPath = Join-Path "." $targetFile
        New-Item -ItemType SymbolicLink -Path $symlinkPath -Target $relativeTargetPath -ErrorAction Stop
        Write-Host "✅ Created symlink: $schemaType/latest.schema.json -> $relativeTargetPath" -ForegroundColor Green
        $successCount++
    }
    catch {
        Write-Host "❌ Error creating symlink for $schemaType : $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
    }
}

# Создаем симлинки для корневых схем (обратная совместимость)
Write-Host "`n🔗 Creating root schema symlinks..." -ForegroundColor Cyan

$rootSymlinks = @{
    "instructions.schema.json" = "deepseek-instructions/latest.schema.json"
    "context_config.schema.json" = "context-config/latest.schema.json"
    "selective_export.schema.json" = "selective-export/latest.schema.json"
    "return_export.schema.json" = "return-export/latest.schema.json"
}

foreach ($symlinkName in $rootSymlinks.Keys) {
    $symlinkPath = Join-Path $schemasPath $symlinkName
    $targetPath = $rootSymlinks[$symlinkName]

    if (Test-Path $symlinkPath) {
        Remove-Item $symlinkPath -Force -ErrorAction SilentlyContinue
    }

    try {
        New-Item -ItemType SymbolicLink -Path $symlinkPath -Target $targetPath -ErrorAction Stop
        Write-Host "✅ Created root symlink: $symlinkName -> $targetPath" -ForegroundColor Green
        $successCount++
    }
    catch {
        Write-Host "⚠️  Could not create root symlink $symlinkName : $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# Сводка
Write-Host "`n📊 Summary:" -ForegroundColor White
Write-Host "✅ Successful: $successCount" -ForegroundColor Green
Write-Host "❌ Errors: $errorCount" -ForegroundColor Red
Write-Host "⚠️  Skipped: $skippedCount" -ForegroundColor Yellow

if ($errorCount -eq 0) {
    Write-Host "`n🎉 Symlink creation completed successfully!" -ForegroundColor Green
}
else {
    Write-Host "`n❌ Symlink creation completed with errors" -ForegroundColor Red
    exit 1
}