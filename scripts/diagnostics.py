# diagnostics.py
import asyncio
from services.config_loader import ValidatedConfigLoader
from pathlib import Path

async def full_diagnostics():
    print("🔧 Полная диагностика системы валидации")
    
    # 1. Проверка существования файлов
    required_dirs = ['instructions', 'configs', 'schemas']
    for dir_name in required_dirs:
        path = Path(dir_name)
        status = "✅" if path.exists() else "❌"
        print(f"{status} {dir_name}/: {path.exists()}")
    
    # 2. Проверка схем
    loader = ValidatedConfigLoader()
    try:
        await loader.initialize()
        print(f"✅ Загружено схем: {len(loader.schema_manager.schemas)}")
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
    
    # 3. Тестовая валидация
    test_files = [
        'instructions/deepseek_instructions_v1.5.json',
        'configs/context_config_test_validation.json'
    ]
    
    for file_path in test_files:
        try:
            if Path(file_path).exists():
                await loader.load_and_validate(file_path)
                print(f"✅ {file_path}")
            else:
                print(f"⚠️  {file_path} (не найден)")
        except Exception as e:
            print(f"❌ {file_path}: {e}")

asyncio.run(full_diagnostics())