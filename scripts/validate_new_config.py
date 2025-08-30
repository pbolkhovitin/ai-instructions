# validate_new_config.py
import asyncio
from services.config_loader import ValidatedConfigLoader

async def validate_new_project():
    loader = ValidatedConfigLoader()
    await loader.initialize()
    
    try:
        config = await loader.load_and_validate(
            'configs/context_config_my-ai-project.json'
        )
        print("✅ Новый конфиг прошел валидацию!")
        return config
    except Exception as e:
        print(f"❌ Ошибка валидации: {e}")
        return None

asyncio.run(validate_new_project())