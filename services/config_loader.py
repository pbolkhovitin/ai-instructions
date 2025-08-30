# services/config_loader.py (дополняем)
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import aiofiles
from .schema_manager import SchemaManager, ConfigValidationError

logger = logging.getLogger(__name__)

# ДОБАВИТЬ этот класс
class ConfigLoadError(Exception):
    """Кастомное исключение для ошибок загрузки конфигурации."""
    pass

class ValidatedConfigLoader:
    """Загрузчик конфигов с валидацией через JSON схемы."""
    
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.schema_manager = SchemaManager(self.base_path / "schemas")
    
    async def initialize(self) -> None:
        """Инициализация загрузчика с загрузкой схем."""
        await self.schema_manager.initialize()
    
    async def load_config(self, relative_path: str) -> Dict[str, Any]:
        """Загружает конфиг без валидации."""
        full_path = self.base_path / relative_path
        
        if not full_path.exists():
            raise ConfigLoadError(f"Файл не найден: {full_path}")  # ИЗМЕНИТЬ здесь
        
        async with aiofiles.open(full_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        return json.loads(content)
    
    async def load_and_validate(self, relative_path: str) -> Dict[str, Any]:
        """Загружает и валидирует конфиг."""
        try:
            config_data = await self.load_config(relative_path)
            
            # Валидируем через SchemaManager
            await self.schema_manager.validate_config(config_data, relative_path)
            
            return config_data
            
        except Exception as e:
            logger.error(f"❌ P0: Ошибка загрузки/валидации конфига {relative_path}: {e}")
            raise ConfigValidationError(f"P0 Validation failed for {relative_path}: {e}")