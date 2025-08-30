#!/usr/bin/env python3
"""
Диагностический тест для проверки структуры и содержимого.
Запуск: python tests/diagnostic_test.py
"""

import os
import sys
import json
from pathlib import Path

# Добавляем корень проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_file_structure():
    """Проверяет базовую структуру файлов."""
    print("🔍 Проверка структуры файлов...")
    
    # Проверяем основные директории
    required_dirs = ['instructions', 'schemas', 'configs', 'scripts', 'tests']
    for dir_name in required_dirs:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path):
            print(f"✅ Директория {dir_name}/ найдена")
        else:
            print(f"❌ Директория {dir_name}/ не найдена")
    
    # Проверяем файл инструкций
    instructions_path = os.path.join(project_root, 'instructions', 'deepseek_instructions_v1.5.json')
    if os.path.exists(instructions_path):
        print(f"✅ Файл инструкций найден: {instructions_path}")
        
        # Проверяем содержимое
        try:
            with open(instructions_path, 'r', encoding='utf-8') as f:
                content = f.read()
                data = json.loads(content)
                
                print(f"📄 Размер файла: {len(content)} символов")
                print(f"✅ Валидный JSON")
                
                # Проверяем обязательные поля
                required_fields = ['config_version', 'protocol_version', 'role', 'protocol']
                for field in required_fields:
                    if field in data:
                        print(f"✅ Поле {field}: {data[field]}")
                    else:
                        print(f"❌ Отсутствует поле: {field}")
                        
        except json.JSONDecodeError as e:
            print(f"❌ Файл не является валидным JSON: {e}")
            return False
        except Exception as e:
            print(f"❌ Ошибка чтения файла: {e}")
            return False
    else:
        print(f"❌ Файл инструкций не найден: {instructions_path}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 ДИАГНОСТИЧЕСКИЙ ТЕСТ")
    print("=" * 60)
    
    success = check_file_structure()
    
    print("=" * 60)
    if success:
        print("🎉 Базовая структура в порядке!")
    else:
        print("❌ Обнаружены проблемы со структурой!")
    print("=" * 60)