# Файл: tests/create_test_schema.py
import json
import os
from pathlib import Path

# Создаем минимальную валидную схему для теста
test_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["config_version", "protocol_version", "role"],
    "properties": {
        "config_version": {"type": "string"},
        "protocol_version": {"type": "string"},
        "role": {"type": "string"},
        "style": {"type": "string"},
        "primary_goal": {"type": "string"},
        "emphasis": {"type": "string"}
    }
}

# Создаем директорию для схем
schemas_dir = Path("schemas/deepseek-instructions")
schemas_dir.mkdir(parents=True, exist_ok=True)

# Сохраняем схему
schema_path = schemas_dir / "v1.5.schema.json"
with open(schema_path, 'w', encoding='utf-8') as f:
    json.dump(test_schema, f, indent=2, ensure_ascii=False)

print(f"✅ Тестовая схема создана: {schema_path}")