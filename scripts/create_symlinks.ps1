# Fixed symlink creation script
Write-Host "Creating symlinks for schemas..." -ForegroundColor Green

$repoPath = "C:\Users\pbolk\Documents\GitHub\ai-instructions"
$schemasPath = Join-Path $repoPath "schemas"

if (-not (Test-Path $schemasPath)) {
    Write-Host "Error: schemas directory not found" -ForegroundColor Red
    exit 1
}

Set-Location $schemasPath

$schemas = @(
    @{Type = "deepseek-instructions"; Version = "v1.5"},
    @{Type = "context-config"; Version = "v1.5"}
)

foreach ($schema in $schemas) {
    $schemaDir = Join-Path $schemasPath $schema.Type
    $targetFile = $schema.Version + ".schema.json"
    $symlinkFile = "latest.schema.json"
    
    if (Test-Path $schemaDir) {
        Set-Location $schemaDir
        
        if (-not (Test-Path $targetFile)) {
            Write-Host "Warning: File $targetFile not found in $($schema.Type)" -ForegroundColor Yellow
            continue
        }
        
        if (Test-Path $symlinkFile) {
            Remove-Item $symlinkFile -Force -ErrorAction SilentlyContinue
            Write-Host "Removed old symlink: $($schema.Type)/$symlinkFile" -ForegroundColor Gray
        }
        
        try {
            New-Item -ItemType SymbolicLink -Name $symlinkFile -Target $targetFile -ErrorAction Stop
            Write-Host "Created symlink: $($schema.Type)/$symlinkFile -> $targetFile" -ForegroundColor Green
        }
        catch {
            Write-Host "Error creating symlink for $($schema.Type): $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "Warning: Directory $($schema.Type) not found" -ForegroundColor Yellow
    }
}

Write-Host "Process completed!" -ForegroundColor Green
Set-Location $repoPath