# services/schema_manager.py
"""
Менеджер JSON схем для валидации конфигурационных файлов.
Поддерживает существующую структуру с версионированием и симлинками.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import jsonschema
from jsonschema import Draft7Validator

logger = logging.getLogger(__name__)

class SchemaManager:
    """Управление JSON схемами для валидации конфигов."""
    
    def __init__(self, schemas_dir: str = "schemas"):
        self.schemas_dir = Path(schemas_dir)
        self.schemas: Dict[str, Dict] = {}
        self.validators: Dict[str, Draft7Validator] = {}
        self.schema_aliases: Dict[str, str] = {}  # Для поддержки симлинков
        
    async def initialize(self) -> None:
        """Инициализация менеджера схем с поддержкой существующей структуры."""
        if not self.schemas_dir.exists():
            logger.warning(f"Директория схем не найдена: {self.schemas_dir}")
            return
        
        await self.load_all_schemas()
        await self.process_symlinks_and_aliases()
    
    async def load_all_schemas(self) -> None:
        """Загружает все JSON схемы из сложной структуры директорий."""
        # Загружаем схемы из context-config/
        context_config_dir = self.schemas_dir / "context-config"
        if context_config_dir.exists():
            await self._load_schemas_from_directory(context_config_dir, "context-config")
        
        # Загружаем схемы из deepseek-instructions/
        instructions_dir = self.schemas_dir / "deepseek-instructions"
        if instructions_dir.exists():
            await self._load_schemas_from_directory(instructions_dir, "deepseek-instructions")
        
        # Загружаем корневые схемы (для обратной совместимости)
        await self._load_root_schemas()
    
    async def _load_schemas_from_directory(self, directory: Path, schema_type: str) -> None:
        """Загружает схемы из конкретной директории типа."""
        for schema_file in directory.glob("*.schema.json"):
            try:
                schema_name = f"{schema_type}_{schema_file.stem.replace('.schema', '')}"
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema_data = json.load(f)
                
                self.schemas[schema_name] = schema_data
                self.validators[schema_name] = Draft7Validator(schema_data)
                logger.info(f"✅ Загружена схема: {schema_name}")
                
            except Exception as e:
                logger.error(f"❌ Ошибка загрузки схемы {schema_file}: {e}")
    
    async def _load_root_schemas(self) -> None:
        """Загружает схемы из корневой директории для обратной совместимости."""
        for schema_file in self.schemas_dir.glob("*.json"):
            if schema_file.name not in ["index.json", "README.md"]:
                try:
                    schema_name = schema_file.stem
                    with open(schema_file, 'r', encoding='utf-8') as f:
                        schema_data = json.load(f)
                    
                    self.schemas[schema_name] = schema_data
                    self.validators[schema_name] = Draft7Validator(schema_data)
                    logger.info(f"✅ Загружена корневая схема: {schema_name}")
                    
                except Exception as e:
                    logger.error(f"❌ Ошибка загрузки корневой схемы {schema_file}: {e}")
    
    async def process_symlinks_and_aliases(self) -> None:
        """Обрабатывает симлинки и создает алиасы для схем."""
        # Обрабатываем latest.schema.json как симлинки на актуальные версии
        for schema_type in ["context-config", "deepseek-instructions"]:
            latest_path = self.schemas_dir / schema_type / "latest.schema.json"
            if latest_path.exists() and latest_path.is_symlink():
                try:
                    target_path = latest_path.resolve()
                    version = target_path.stem.replace('.schema', '')
                    alias_name = f"{schema_type}_latest"
                    target_name = f"{schema_type}_{version}"
                    
                    if target_name in self.schemas:
                        self.schemas[alias_name] = self.schemas[target_name]
                        self.validators[alias_name] = self.validators[target_name]
                        self.schema_aliases[alias_name] = target_name
                        logger.info(f"✅ Создан алиас: {alias_name} -> {target_name}")
                        
                except Exception as e:
                    logger.error(f"❌ Ошибка обработки симлинка {latest_path}: {e}")
        
        # Создаем алиасы для корневых схем
        root_aliases = {
            "instructions": "deepseek-instructions_latest",
            "context_config": "context-config_latest"
        }
        
        for alias, target in root_aliases.items():
            if target in self.schemas:
                self.schemas[alias] = self.schemas[target]
                self.validators[alias] = self.validators[target]
                self.schema_aliases[alias] = target
                logger.info(f"✅ Создан корневой алиас: {alias} -> {target}")
    
    def get_schema_type(self, config_data: Dict[str, Any]) -> Optional[str]:
        """Определяет тип схемы на основе данных конфига."""
        # Сначала проверяем явные типы (selective_export и return_export)
        config_type = config_data.get('type')
        if config_type == 'selective_export':
            # Дополнительная проверка для selective_export
            if 'selected_topic' in config_data and 'parent_topic' in config_data:
                return 'selective_export'
        
        if config_type == 'return_export':
            # Дополнительная проверка для return_export
            if 'results_summary' in config_data and 'key_decisions' in config_data:
                return 'return_export'
        
        # Если это конфиг контекста (имеет meta и core_topic)
        if 'meta' in config_data and isinstance(config_data['meta'], dict):
            meta = config_data['meta']
            if 'core_topic' in meta:
                return 'context_config'
        
        # Если это инструкции (имеет protocol_version)
        if 'protocol_version' in config_data:
            return 'instructions'
        
        return None
    
    async def validate_config(self, config_data: Dict[str, Any], config_path: str) -> None:
        """
        Валидирует конфиг по соответствующей JSON схеме.
        
        Args:
            config_data: Данные конфигурации
            config_path: Путь к конфигу (для логирования)
        
        Raises:
            ConfigValidationError: Если валидация не пройдена
        """
        schema_type = self.get_schema_type(config_data)
        
        if not schema_type:
            logger.warning(f"⚠️  Не удалось определить тип схемы для {config_path}")
            return
        
        if schema_type not in self.validators:
            logger.warning(f"⚠️  Схема {schema_type} не найдена для валидации {config_path}")
            # Попробуем определить версию и использовать конкретную схему
            await self._validate_with_version_fallback(config_data, config_path, schema_type)
            return
        
        validator = self.validators[schema_type]
        
        try:
            validator.validate(config_data)
            actual_schema = self.schema_aliases.get(schema_type, schema_type)
            logger.info(f"✅ Валидация пройдена: {config_path} -> {actual_schema}")
            
        except jsonschema.ValidationError as e:
            error_msg = self._format_validation_error(e, config_path, schema_type)
            logger.error(f"❌ Ошибка валидации: {error_msg}")
            raise ConfigValidationError(error_msg)
    
    async def _validate_with_version_fallback(self, config_data: Dict[str, Any], 
                                            config_path: str, schema_type: str) -> None:
        """Попытка валидации с определением версии."""
        version = config_data.get('config_version', '1.5')
        specific_schema = f"{schema_type}_{version}"
        
        if specific_schema in self.validators:
            validator = self.validators[specific_schema]
            try:
                validator.validate(config_data)
                logger.info(f"✅ Валидация пройдена (fallback): {config_path} -> {specific_schema}")
                return
            except jsonschema.ValidationError as e:
                error_msg = self._format_validation_error(e, config_path, specific_schema)
                logger.error(f"❌ Ошибка валидации (fallback): {error_msg}")
                raise ConfigValidationError(error_msg)
        
        raise ConfigValidationError(f"Не найдена подходящая схема для {config_path}. "
                                  f"Тип: {schema_type}, Версия: {version}")
    
    def _format_validation_error(self, error: jsonschema.ValidationError, 
                               config_path: str, schema_type: str) -> str:
        """Форматирует сообщение об ошибке валидации."""
        path = ".".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
        actual_schema = self.schema_aliases.get(schema_type, schema_type)
        
        return (f"Validation failed for {config_path} (schema: {actual_schema})\n"
                f"Path: {path}\n"
                f"Error: {error.message}\n"
                f"Value: {error.instance}")

class ConfigValidationError(Exception):
    """Исключение для ошибок валидации конфигурации."""
    pass