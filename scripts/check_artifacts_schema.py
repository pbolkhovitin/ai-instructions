# scripts/check_artifacts_schema.py
import json
from pathlib import Path

def check_artifacts_schema():
    """Проверяет точную структуру, которую ожидает схема для artifacts."""
    schema_path = Path("schemas/context-config/v1.5.schema.json")
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    
    # Смотрим точное определение artifacts
    artifacts_def = schema['properties']['key_data']['properties']['artifacts']
    print("📋 Требования к artifacts:")
    print(f"   Тип: {artifacts_def.get('type')}")
    print(f"   Описание: {artifacts_def.get('description', 'нет')}")
    
    # Проверяем items если это массив
    if 'items' in artifacts_def:
        print(f"   Элементы: {artifacts_def['items']}")
    else:
        print("   ❌ Нет определения элементов массива")

if __name__ == "__main__":
    check_artifacts_schema()