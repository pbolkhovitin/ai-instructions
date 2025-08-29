#!/usr/bin/env python3
"""
Тестирование P0 автоматической валидации конфигов.
Запуск: python tests/test_p0_validation.py
"""

import asyncio
import sys
import os
from pathlib import Path

# Добавляем корень проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from services.config_loader import ValidatedConfigLoader, ConfigValidationError
    print("✅ Модули успешно импортированы")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("📁 Текущая структура проекта:")
    for root, dirs, files in os.walk(project_root):
        level = root.replace(str(project_root), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f'{subindent}{file}')
    sys.exit(1)

async def test_p0_validation():
    """Тестирование P0 автоматической валидации."""
    print("🧪 Тестирование P0 автоматической валидации конфигов...")
    print(f"📁 Рабочая директория: {os.getcwd()}")
    
    loader = ValidatedConfigLoader()
    
    try:
        # Проверяем существование файлов
        instructions_path = os.path.join(loader.base_path, 'instructions', 'deepseek_instructions_v1.5.json')
        if not os.path.exists(instructions_path):
            print(f"❌ Файл инструкций не найден: {instructions_path}")
            return False
        
        print("✅ Файл инструкций найден")
        
        # Тестируем загрузку с валидацией
        instructions = await loader.load_and_validate('instructions/deepseek_instructions_v1.5.json')
        print("✅ P0: Валидация инструкций прошла успешно")
        
        # Проверяем существование configs директории
        configs_dir = os.path.join(loader.base_path, 'configs')
        if not os.path.exists(configs_dir):
            print(f"⚠️  Директория configs не найдена: {configs_dir}")
            print("✅ P0: Основная валидация инструкций работает")
            return True
        
        # Тестируем загрузку конфигов контекста
        config_files = []
        for file in os.listdir(configs_dir):
            if file.endswith('.json') and file.startswith('context_config_'):
                config_files.append(file)
        
        if not config_files:
            print("⚠️  Конфиги контекста не найдены в директории configs")
            print("✅ P0: Основная валидация инструкций работает")
            return True
        
        for config_file in config_files:
            config_path = f'configs/{config_file}'
            config = await loader.load_and_validate(config_path)
            print(f"✅ P0: Валидация {config_path} прошла успешно")
        
        print("🎉 P0: Все тесты автоматической валидации пройдены!")
        return True
        
    except ConfigValidationError as e:
        print(f"❌ P0: Ошибка валидации конфига: {e}")
        return False
    except Exception as e:
        print(f"❌ P0: Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 ЗАПУСК ТЕСТА P0 ВАЛИДАЦИИ")
    print("=" * 60)
    
    success = asyncio.run(test_p0_validation())
    
    print("=" * 60)
    if success:
        print("🎉 ТЕСТ ПРОЙДЕН УСПЕШНО!")
    else:
        print("❌ ТЕСТ ПРОВАЛЕН!")
    print("=" * 60)
    
    sys.exit(0 if success else 1)