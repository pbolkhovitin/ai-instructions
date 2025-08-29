# Скрипт для создания симлинков в Windows
Write-Host "🔗 Создание симлинков для схем..." -ForegroundColor Green

# Переходим в директорию схем
$repoPath = "C:\Users\pbolk\Documents\GitHub\ai-instructions"
$schemasPath = Join-Path $repoPath "schemas"

if (-not (Test-Path $schemasPath)) {
    Write-Host "❌ Директория schemas не найдена" -ForegroundColor Red
    exit 1
}

Set-Location $schemasPath

# Создаем симлинки для каждой схемы
$schemas = @(
    @{Type = "deepseek-instructions"; Version = "v1.5"},
    @{Type = "context-config"; Version = "v1.5"}
)

foreach ($schema in $schemas) {
    $schemaDir = Join-Path $schemasPath $schema.Type
    $targetFile = "$($schema.Version).schema.json"
    $symlinkFile = "latest.schema.json"
    $fullSymlinkPath = Join-Path $schemaDir $symlinkPath
    
    if (Test-Path $schemaDir) {
        Set-Location $schemaDir
        
        # Проверяем существует ли целевой файл
        if (-not (Test-Path $targetFile)) {
            Write-Host "⚠️  Файл $targetFile не найден в $($schema.Type)" -ForegroundColor Yellow
            continue
        }
        
        # Удаляем старый симлинк если существует
        if (Test-Path $symlinkFile) {
            Remove-Item $symlinkFile -Force
            Write-Host "🗑️  Удален старый симлинк: $($schema.Type)/$symlinkFile" -ForegroundColor Gray
        }
        
        # Создаем новый симлинк
        try {
            New-Item -ItemType SymbolicLink -Name $symlinkFile -Target $targetFile
            Write-Host "✅ Создан симлинк: $($schema.Type)/$symlinkFile -> $targetFile" -ForegroundColor Green
        }
        catch {
            Write-Host "❌ Ошибка создания симлинка для $($schema.Type): $_" -ForegroundColor Red
        }
    }
    else {
        Write-Host "⚠️  Директория $($schema.Type) не найдена" -ForegroundColor Yellow
    }
}

Write-Host "`n🎉 Процесс завершен!" -ForegroundColor Green
Set-Location $repoPath