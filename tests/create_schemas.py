#!/usr/bin/env python3
"""
Создание базовых JSON схем для тестирования.
Запуск: python tests/create_schemas.py
"""

import json
import os
from pathlib import Path

# Базовая схема для инструкций
instructions_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["config_version", "protocol_version", "role", "primary_goal", "protocol"],
    "properties": {
        "config_version": {"type": "string"},
        "protocol_version": {"type": "string"},
        "role": {"type": "string"},
        "style": {"type": "string"},
        "primary_goal": {"type": "string"},
        "emphasis": {"type": "string"},
        "protocol": {"type": "object"},
        "commands": {"type": "object"},
        "principles": {"type": "object"},
        "confirmation": {"type": "string"}
    }
}

# Базовая схема для конфигов контекста
context_config_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["config_version", "type", "meta", "key_data", "parent_settings"],
    "properties": {
        "config_version": {"type": "string"},
        "type": {"type": "string"},
        "parent_topic": {"type": "string"},
        "selected_topic": {"type": "string"},
        "meta": {
            "type": "object",
            "required": ["core_topic", "conversation_style", "user_profile"],
            "properties": {
                "core_topic": {"type": "string"},
                "conversation_style": {"type": "string"},
                "user_profile": {"type": "string"},
                "branch_id": {"type": "string"}
            }
        },
        "key_data": {
            "type": "object",
            "required": ["achievements", "constraints", "important_facts", "artifacts"],
            "properties": {
                "achievements": {"type": "array", "items": {"type": "string"}},
                "constraints": {"type": "array", "items": {"type": "string"}},
                "important_facts": {"type": "array", "items": {"type": "string"}},
                "artifacts": {"type": "array", "items": {"type": "string"}}
            }
        },
        "parent_settings": {
            "type": "object",
            "required": ["auto_summary_enabled", "auto_summary_interval", "default_response_format", "verbosity_level"],
            "properties": {
                "auto_summary_enabled": {"type": "boolean"},
                "auto_summary_interval": {"type": "integer"},
                "default_response_format": {"type": "string"},
                "verbosity_level": {"type": "string"}
            }
        }
    }
}

# Создаем директории схем
schemas_dir = Path("schemas")
schemas_dir.mkdir(exist_ok=True)

instructions_schema_dir = schemas_dir / "deepseek-instructions"
instructions_schema_dir.mkdir(exist_ok=True)

context_schema_dir = schemas_dir / "context-config" 
context_schema_dir.mkdir(exist_ok=True)

# Сохраняем схемы
instructions_schema_path = instructions_schema_dir / "v1.5.schema.json"
with open(instructions_schema_path, 'w', encoding='utf-8') as f:
    json.dump(instructions_schema, f, indent=2, ensure_ascii=False)

context_schema_path = context_schema_dir / "v1.5.schema.json"
with open(context_schema_path, 'w', encoding='utf-8') as f:
    json.dump(context_config_schema, f, indent=2, ensure_ascii=False)

print(f"✅ Схема инструкций создана: {instructions_schema_path}")
print(f"✅ Схема конфигов создана: {context_schema_path}")
print("🎉 Базовая схема готова для тестирования!")