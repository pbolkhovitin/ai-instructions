#!/usr/bin/env python3
"""
Скрипт для автоматического создания и обновления индекса схем.
Генерирует schemas/index.json с информацией о всех доступных схемах.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

def generate_schemas_index(base_path: str) -> Dict[str, Any]:
    """
    Генерирует индексный файл со всеми схемами в репозитории.
    
    Args:
        base_path: Путь к корню репозитория
    
    Returns:
        Словарь с индексом всех схем
    """
    schemas_dir = Path(base_path) / "schemas"
    index_data = {
        "version": "1.0",
        "generated_at": "",  # Заполнится автоматически
        "schemas": {}
    }
    
    if not schemas_dir.exists():
        print(f"❌ Директория schemas/ не найдена")
        return index_data
    
    import datetime
    index_data["generated_at"] = datetime.datetime.now().isoformat()
    
    # Рекурсивный поиск всех .schema.json файлов
    schema_files = list(schemas_dir.rglob("*.schema.json"))
    
    for schema_file in schema_files:
        if schema_file.name == "latest.schema.json":
            continue  # Пропускаем симлинки
        
        # Определяем тип схемы из пути
        relative_path = schema_file.relative_to(schemas_dir)
        schema_type = relative_path.parent.name
        version = schema_file.stem.replace(".schema", "")  # v1.5
        
        # Читаем базовую информацию из схемы
        schema_info = {
            "version": version,
            "path": str(relative_path),
            "file_size": schema_file.stat().st_size,
            "last_modified": schema_file.stat().st_mtime
        }
        
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_content = json.load(f)
                schema_info["title"] = schema_content.get("title", "")
                schema_info["description"] = schema_content.get("description", "")
        except Exception as e:
            schema_info["load_error"] = str(e)
        
        # Добавляем в индекс
        if schema_type not in index_data["schemas"]:
            index_data["schemas"][schema_type] = {
                "latest": version,
                "versions": [],
                "schemas": {}
            }
        
        index_data["schemas"][schema_type]["versions"].append(version)
        index_data["schemas"][schema_type]["schemas"][version] = schema_info
    
    # Сортируем версии и определяем latest
    for schema_type, type_data in index_data["schemas"].items():
        if type_data["versions"]:
            # Сортируем версии по числовому значению
            sorted_versions = sorted(type_data["versions"], 
                                   key=lambda x: [int(num) for num in x[1:].split('.')])
            type_data["latest"] = sorted_versions[-1]  # Последняя версия
            type_data["versions"] = sorted_versions
    
    return index_data

def update_latest_symlinks(base_path: str, index_data: Dict[str, Any]):
    """
    Обновляет симлинки latest.schema.json на основе индекса.
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
                    
                    # Создаем новый симлинк
                    symlink_file.symlink_to(latest_file.name)
                    print(f"✅ Обновлен симлинк: {schema_type}/latest.schema.json -> {latest_version}.schema.json")
                    
                except Exception as e:
                    print(f"❌ Ошибка создания симлинка для {schema_type}: {e}")
            else:
                print(f"⚠️  Файл {latest_file} не существует")

def main():
    """Основная функция скрипта."""
    repo_path = "C:/Users/pbolk/Documents/GitHub/ai-instructions"
    schemas_dir = Path(repo_path) / "schemas"
    
    if not schemas_dir.exists():
        print("❌ Директория schemas/ не найдена")
        sys.exit(1)
    
    print("🔍 Генерация индекса схем...")
    
    # Генерируем индекс
    index_data = generate_schemas_index(repo_path)
    
    # Сохраняем индекс
    index_file = schemas_dir / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Индекс схем сохранен: schemas/index.json")
    print(f"📊 Найдено типов схем: {len(index_data['schemas'])}")
    
    for schema_type, data in index_data["schemas"].items():
        print(f"   - {schema_type}: {len(data['versions'])} версий, latest: {data['latest']}")
    
    # Обновляем симлинки
    print("\n🔗 Обновление симлинков latest...")
    update_latest_symlinks(repo_path, index_data)
    
    print(f"\n🎉 Индекс схем успешно обновлен!")

if __name__ == "__main__":
    main()