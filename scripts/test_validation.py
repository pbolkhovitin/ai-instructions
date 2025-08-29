#!/usr/bin/env python3
"""
Тестовый скрипт для проверки валидации.
"""

from validate_config import validate_config

def test_validation():
    """Тестирует валидацию на всех доступных конфигах."""
    from pathlib import Path
    import glob
    
    print("🧪 Запуск тестов валидации...")
    
    # Тестируем все конфиги
    config_files = glob.glob("configs/*.json")
    
    if not config_files:
        print("⚠️  Тестовые конфиги не найдены")
        return False
    
    results = []
    for config_file in config_files:
        print(f"\n🔍 Тестируем: {Path(config_file).name}")
        result = validate_config(config_file)
        results.append(result)
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 Результаты: {success_count}/{total_count} тестов пройдено")
    
    if success_count == total_count:
        print("🎉 Все тесты прошли успешно!")
        return True
    else:
        print("❌ Некоторые тесты не прошли!")
        return False

if __name__ == "__main__":
    success = test_validation()
    sys.exit(0 if success else 1)