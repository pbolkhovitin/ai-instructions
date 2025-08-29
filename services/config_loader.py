import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import aiohttp
import aiofiles
from aiohttp import ClientConnectorError
import jsonschema
from jsonschema import validate, ValidationError

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigLoadError(Exception):
    """Кастомное исключение для ошибок загрузки конфигурации."""
    pass

class ConfigValidationError(Exception):
    """Кастомное исключение для ошибок валидации конфигурации."""
    pass

async def load_from_local_or_github(local_path: str, github_url: str) -> str:
    """
    Универсальная функция загрузки. Сначала пробует локальный путь,
    затем GitHub RAW в качестве fallback.
    """
    local_file = Path(local_path)
    if local_file.is_file():
        try:
            async with aiofiles.open(local_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                logger.info(f"Успешно загружено из локального файла: {local_path}")
                return content
        except IOError as e:
            logger.warning(f"Не удалось прочитать локальный файл {local_path}: {e}. Пробуем GitHub...")
    
    # Fallback: Загрузка с GitHub RAW
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(github_url) as response:
                if response.status == 200:
                    content = await response.text()
                    logger.info(f"Успешно загружено с GitHub: {github_url}")
                    return content
                else:
                    raise ConfigLoadError(f"GitHub вернул статус {response.status} для URL {github_url}")
    except ClientConnectorError as e:
        raise ConfigLoadError(f"Не удалось подключиться к GitHub для загрузки. Ошибка сети: {e}")
    except Exception as e:
        raise ConfigLoadError(f"Неожиданная ошибка при загрузке с GitHub: {e}")

class SchemaManager:
    """Менеджер для загрузки и валидации JSON Schema."""
    
    def __init__(self, base_local_path: str = "C:/Users/pbolk/Documents/GitHub/ai-instructions"):
        self.base_local_path = base_local_path
        self._schemas_cache: Dict[str, Dict] = {}
    
    async def get_schema(self, schema_type: str, version: str) -> Dict[str, Any]:
        """Загружает JSON Schema для указанного типа и версии."""
        cache_key = f"{schema_type}_{version}"
        if cache_key in self._schemas_cache:
            return self._schemas_cache[cache_key]
        
        local_schema_path = os.path.join(self.base_local_path, 'schemas', schema_type, f'v{version}.schema.json')
        github_schema_url = f'https://raw.githubusercontent.com/pbolkhovitin/ai-instructions/main/schemas/{schema_type}/v{version}.schema.json'
        
        schema_json = await load_from_local_or_github(local_schema_path, github_schema_url)
        schema_data = json.loads(schema_json)
        
        self._schemas_cache[cache_key] = schema_data
        return schema_data
    
    async def validate_config(self, config_data: Dict, schema_type: str, version: str) -> bool:
        """Валидирует конфигурационные данные против схемы."""
        try:
            schema = await self.get_schema(schema_type, version)
            validate(instance=config_data, schema=schema)
            logger.info(f"Конфиг успешно прошел валидацию против схемы {schema_type} v{version}")
            return True
        except ValidationError as e:
            logger.error(f"Ошибка валидации конфига: {e.message}")
            raise ConfigValidationError(f"Ошибка валидации: {e.message}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка при валидации: {e}")
            raise ConfigValidationError(f"Ошибка валидации: {e}")

class InstructionLoader:
    """Загрузчик для файлов базовых инструкций ассистента."""
    
    def __init__(self, base_local_path: str = "C:/Users/pbolk/Documents/GitHub/ai-instructions"):
        self.base_local_path = base_local_path
        self.schema_manager = SchemaManager(base_local_path)
    
    async def load_and_validate_instructions(self, version: str = "1.5") -> Dict[str, Any]:
        """Загружает и валидирует файл базовых инструкций."""
        local_path = os.path.join(self.base_local_path, 'instructions', f'deepseek_instructions_v{version}.json')
        github_url = f'https://raw.githubusercontent.com/pbolkhovitin/ai-instructions/main/instructions/deepseek_instructions_v{version}.json'
        
        instructions_json = await load_from_local_or_github(local_path, github_url)
        instructions_data = json.loads(instructions_json)
        
        # Валидация против схемы
        await self.schema_manager.validate_config(instructions_data, 'deepseek-instructions', version)
        
        return instructions_data

class ContextConfigLoader:
    """Загрузчик для конфигов контекста."""
    
    def __init__(self, base_local_path: str = "C:/Users/pbolk/Documents/GitHub/ai-instructions"):
        self.base_local_path = base_local_path
        self.schema_manager = SchemaManager(base_local_path)
    
    async def load_and_validate_config(self, config_name: str) -> Dict[str, Any]:
        """Загружает и валидирует конфиг контекста."""
        local_path = os.path.join(self.base_local_path, 'configs', config_name)
        github_url = f'https://raw.githubusercontent.com/pbolkhovitin/ai-instructions/main/configs/{config_name}'
        
        config_json = await load_from_local_or_github(local_path, github_url)
        config_data = json.loads(config_json)
        
        # Определяем тип схемы на основе содержимого конфига
        config_type = config_data.get('type', 'full_export')
        schema_type = 'context-config'
        version = config_data.get('config_version', '1.5')
        
        await self.schema_manager.validate_config(config_data, schema_type, version)
        
        return config_data

# Фабрика для создания загрузчиков
class ConfigLoaderFactory:
    """Фабрика для создания и управления загрузчиками."""
    
    _instance = None
    
    def __new__(cls, base_path: str = "C:/Users/pbolk/Documents/GitHub/ai-instructions"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.base_path = base_path
            cls._instance.schema_manager = SchemaManager(base_path)
            cls._instance.instruction_loader = InstructionLoader(base_path)
            cls._instance.context_loader = ContextConfigLoader(base_path)
        return cls._instance
    
    async def initialize(self):
        """Инициализация всех загрузчиков."""
        try:
            # Предзагрузка схем для кэширования
            await self.schema_manager.get_schema('deepseek-instructions', '1.5')
            await self.schema_manager.get_schema('context-config', '1.5')
            logger.info("Все схемы успешно предзагружены и закэшированы")
        except Exception as e:
            logger.error(f"Ошибка предзагрузки схем: {e}")
            raise

# Пример использования в основном приложении
async def main():
    """Пример использования в основном приложении."""
    try:
        # Инициализация фабрики
        factory = ConfigLoaderFactory()
        await factory.initialize()
        
        # Загрузка и валидация базовых инструкций
        instructions = await factory.instruction_loader.load_and_validate_instructions('1.5')
        logger.info("Базовые инструкции успешно загружены и провалидированы")
        
        # Загрузка конкретного конфига контекста
        context_config = await factory.context_loader.load_and_validate_config(
            'context_config_rekomendacii-po-itogam-testirovaniya-protokola-v1-5.json'
        )
        logger.info("Конфиг контекста успешно загружен и провалидирован")
        
        return instructions, context_config
        
    except ConfigLoadError as e:
        logger.error(f"Ошибка загрузки конфигурации: {e}")
        # Можно использовать fallback-конфиги
    except ConfigValidationError as e:
        logger.error(f"Ошибка валидации конфигурации: {e}")
        # Нельзя использовать невалидные конфиги
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

# Добавляем класс ValidatedConfigLoader после существующих классов
class ValidatedConfigLoader:
    """Загрузчик конфигов с автоматической валидацией P0."""
    
    def __init__(self, base_path: str = "C:/Users/pbolk/Documents/GitHub/ai-instructions"):
        self.base_path = base_path
        self.schema_manager = SchemaManager(base_path)
        self.loaded_configs = {}
    
    async def load_and_validate(self, config_path: str, expected_type: str = None) -> Dict[str, Any]:
        """
        Загружает и валидирует конфигурационный файл (P0 реализация).
        
        Args:
            config_path: Относительный путь к конфигу
            expected_type: Ожидаемый тип конфига ('context-config', 'deepseek-instructions')
        
        Returns:
            Валидированный конфиг
        """
        full_path = os.path.join(self.base_path, config_path)
        
        try:
            # Загрузка конфига
            async with aiofiles.open(full_path, 'r', encoding='utf-8') as f:
                config_content = await f.read()
            config_data = json.loads(config_content)
            
            # Определение типа и версии для валидации
            config_version = config_data.get('config_version', '1.5')
            
            if expected_type:
                schema_type = expected_type
            else:
                # Автоопределение типа по имени файла
                if 'deepseek_instructions' in config_path:
                    schema_type = 'deepseek-instructions'
                else:
                    schema_type = 'context-config'
            
            # Валидация против схемы
            await self.schema_manager.validate_config(config_data, schema_type, config_version)
            
            logger.info(f"✅ P0: Конфиг {config_path} успешно загружен и провалидирован")
            self.loaded_configs[config_path] = config_data
            return config_data
            
        except Exception as e:
            logger.error(f"❌ P0: Ошибка загрузки/валидации конфига {config_path}: {e}")
            raise ConfigValidationError(f"P0 Validation failed for {config_path}: {e}")

# Интеграция в основной код ассистента
async def load_assistant_config():
    """Основная функция загрузки конфигурации ассистента с валидацией P0."""
    loader = ValidatedConfigLoader()
    
    try:
        # Загрузка базовых инструкций с валидацией
        instructions = await loader.load_and_validate(
            'instructions/deepseek_instructions_v1.5.json',
            'deepseek-instructions'
        )
        
        # Автоматическая загрузка всех конфигов из директории configs
        configs_dir = os.path.join(loader.base_path, 'configs')
        if os.path.exists(configs_dir):
            for config_file in os.listdir(configs_dir):
                if config_file.endswith('.json'):
                    config_path = os.path.join('configs', config_file)
                    await loader.load_and_validate(config_path)
        
        logger.info("✅ P0: Все конфиги успешно загружены и провалидированы")
        return loader.loaded_configs
        
    except Exception as e:
        logger.error(f"❌ P0: Критическая ошибка загрузки конфигурации: {e}")
        # Fallback: можно загрузить базовые конфиги без валидации
        return await fallback_load()

    async def fallback_load():
        """Fallback загрузка без валидации."""
        logger.warning("⚠️  Используется fallback загрузка без валидации")
        # ... implementation of basic loading without validation
        # В конец config_loader.py добавляем
    async def main():
        """Основная функция с поддержкой P0/P1."""
        try:
            # P0: Загрузка с автоматической валидацией
            loader = ValidatedConfigLoader()
            configs = await loader.load_and_validate('instructions/deepseek_instructions_v1.5.json')
            
            # P1: Аудит репозитория с игнорированием симлинков
            from scripts.repo_audit import RepoAuditor
            auditor = RepoAuditor(loader.base_path)
            audit_results = auditor.run_audit()
            
            print("🎉 P0 и P1 рекомендации успешно внедрены!")
            return configs, audit_results
            
        except Exception as e:
            logger.error(f"Ошибка внедрения P0/P1: {e}")
            raise