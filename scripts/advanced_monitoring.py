# advanced_monitoring.py
import logging
from services.config_loader import ValidatedConfigLoader

# Настройка детального логирования
logging.basicConfig(level=logging.DEBUG)

async def monitored_validation():
    loader = ValidatedConfigLoader()
    
    # Добавляем кастомный обработчик ошибок
    try:
        await loader.initialize()
        config = await loader.load_and_validate('configs/context_config_my-ai-project.json')
        
        # Мониторинг успешной валидации
        print("📊 Статистика валидации:")
        print(f"Загружено схем: {len(loader.schema_manager.schemas)}")
        print(f"Доступные валидаторы: {list(loader.schema_manager.validators.keys())}")
        
        return config
        
    except Exception as e:
        logging.error(f"Критическая ошибка валидации: {e}")
        # Отправка уведомления или fallback
        return await load_fallback_config()

async def load_fallback_config():
    """Fallback стратегия при критических ошибках"""
    print("⚠️  Использование fallback конфигурации")
    # Возвращаем базовый конфиг или значения по умолчанию
    return {
        "meta": {"core_topic": "Fallback режим"},
        "key_data": {"achievements": [], "constraints": []}
    }