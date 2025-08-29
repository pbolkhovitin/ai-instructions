def update_latest_symlinks(base_path: str, index_data: Dict[str, Any]):
    """
    Обновляет симлинки latest.schema.json на основе индекса.
    Поддерживает Windows PowerShell и Unix системы.
    """
    schemas_dir = Path(base_path) / "schemas"
    
    for schema_type, type_data in index_data["schemas"].items():
        latest_version = type_data["latest"]
        schema_dir = schemas_dir / schema_type
        
        if schema_dir.exists():
            latest_file = schema_dir / f"{latest_version}.schema.json"
            symlink_file = schema_dir / "latest.schema.json"
            
            if latest_file.exists():
                try:
                    # Удаляем старый симлинк если существует
                    if symlink_file.exists():
                        symlink_file.unlink()
                    
                    # Создаем симлинк (кроссплатформенный подход)
                    import os
                    if os.name == 'nt':  # Windows
                        import subprocess
                        # Используем PowerShell для создания симлинка
                        subprocess.run([
                            'powershell', '-Command',
                            f'New-Item -ItemType SymbolicLink -Path "{symlink_file}" -Target "{latest_file.name}"'
                        ], check=True, cwd=schema_dir)
                    else:  # Unix/Linux/Mac
                        symlink_file.symlink_to(latest_file.name)
                    
                    print(f"✅ Обновлен симлинк: {schema_type}/latest.schema.json -> {latest_version}.schema.json")
                    
                except Exception as e:
                    print(f"❌ Ошибка создания симлинка для {schema_type}: {e}")
            else:
                print(f"⚠️  Файл {latest_file} не существует")