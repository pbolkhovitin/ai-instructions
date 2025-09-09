#!/usr/bin/env python3
"""
Скрипт для валидации конфигурационных файлов против JSON-схем.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

try:
    import jsonschema
except ImportError:
    print("❌ Требуется установить jsonschema: pip install jsonschema")
    sys.exit(1)

def validate_config(config_path: str, schema_type: str = "context-config") -> bool:
    """
    Валидирует конфигурационный файл против соответствующей схемы.
    
    Args:
        config_path: Путь к конфигурационному файлу
        schema_type: Тип схемы ('context-config' или 'deepseek-instructions')
    
    Returns:
        True если валидно, False если есть ошибки
    """
    try:
        # Загружаем конфиг
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Определяем путь к схеме через симлинк latest
        schema_path = Path("schemas") / schema_type / "latest.schema.json"
        
        if not schema_path.exists():
            print(f"❌ Схема не найдена: {schema_path}")
            return False
        
        # Загружаем схему
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_data = json.load(f)
        
        # Валидируем
        jsonschema.validate(config_data, schema_data)
        print(f"✅ {Path(config_path).name} валиден против {schema_type} схемы")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка JSON в файле {config_path}: {e}")
        return False
    except jsonschema.ValidationError as e:
        print(f"❌ Ошибка валидации {config_path}:")
        print(f"   Поле: {e.json_path}")
        print(f"   Ошибка: {e.message}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка при валидации {config_path}: {e}")
        return False

def detect_schema_type(filename: str) -> str | None:
    """
    Определяет тип JSON-схемы на основе имени файла.
    """
    if filename.startswith('context_config_') or filename == 'context_config.json':
        return "context-config"
    elif filename.startswith('deepseek_instructions_'):
        return "deepseek-instructions"
    # github_config.json не валидируем, пропускаем
    return None  # Неизвестный тип, пропустить

def validate_all_configs(config_pattern: str = "configs/*.json") -> bool:
    """
    Валидирует все конфиги по указанному шаблону.
    
    Returns:
        True если все конфиги валидны, False если есть ошибки
    """
    from glob import glob
    
    config_files = glob(config_pattern)
    if not config_files:
        print(f"⚠️  Конфиги не найдены по шаблону: {config_pattern}")
        return True
    
    print(f"🔍 Найдено конфигов для валидации: {len(config_files)}")
    
    all_valid = True
    for config_file in config_files:
        schema_type = detect_schema_type(Path(config_file).name)
        if schema_type is None:
            print(f"⚠️  Пропуск {config_file}: неизвестный тип конфига")
            continue
        if not validate_config(config_file, schema_type):
            all_valid = False
    
    return all_valid

def main():
    """Основная функция скрипта."""
    if len(sys.argv) > 1:
        # Валидируем указанные файлы
        all_valid = True
        for config_pattern in sys.argv[1:]:
            if not validate_all_configs(config_pattern):
                all_valid = False
    else:
        # Валидируем все конфиги в configs/
        all_valid = validate_all_configs()
    
    if all_valid:
        print("\n🎉 Все конфиги прошли валидацию успешно!")
        sys.exit(0)
    else:
        print("\n❌ Обнаружены ошибки валидации!")
        sys.exit(1)

if __name__ == "__main__":
    main()