# Файл: tests/create_test_config.py
import json
import os
from pathlib import Path

# Создаем тестовый конфиг
test_config = {
    "config_version": "1.5.1",
    "type": "test_export",
    "meta": {
        "core_topic": "Тестовый конфиг для P0 валидации",
        "conversation_style": "технический",
        "user_profile": "Тестировщик"
    },
    "key_data": {
        "achievements": ["Тестовая achievement"],
        "constraints": ["Тестовое ограничение"],
        "important_facts": ["Тестовый факт"]
    },
    "parent_settings": {
        "auto_summary_enabled": True,
        "auto_summary_interval": 3,
        "default_response_format": "markdown",
        "verbosity_level": "normal"
    }
}

# Сохраняем в configs директорию
configs_dir = Path("configs")
configs_dir.mkdir(exist_ok=True)

config_path = configs_dir / "context_config_test_validation.json"
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(test_config, f, indent=2, ensure_ascii=False)

print(f"✅ Тестовый конфиг создан: {config_path}")