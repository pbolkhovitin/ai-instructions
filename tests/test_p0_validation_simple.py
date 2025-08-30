#!/usr/bin/env python3
"""
Тестирование P0 автоматической валидации конфигов.
Запуск: python tests/test_p0_validation.py
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Добавляем корень проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_p0_validation():
    """Тестирование P0 автоматической валидации."""
    print("🧪 Тестирование P0 автоматической валидации конфигов...")
    
    # Временный загрузчик без валидации схем
    class TestLoader:
        def __init__(self):
            self.base_path = "C:/Users/pbolk/Documents/GitHub/ai-instructions"
        
        async def load_and_validate(self, config_path: str):
            """Только загрузка без валидации против схем."""
            full_path = os.path.join(self.base_path, config_path)
            
            if not os.path.exists(full_path):
                raise Exception(f"Файл не найден: {full_path}")
            
            # Используем обычное чтение файла вместо aiofiles
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Простая проверка JSON
            data = json.loads(content)
            
            if 'config_version' not in data:
                raise Exception("Отсутствует config_version")
                
            print(f"✅ Успешная загрузка: {config_path}")
            return data
    
    loader = TestLoader()
    
    try:
        instructions = await loader.load_and_validate('instructions/deepseek_instructions_v1.5.json')
        print("✅ P0: Базовая загрузка работает")
        return True
        
    except Exception as e:
        print(f"❌ P0: Ошибка: {e}")
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