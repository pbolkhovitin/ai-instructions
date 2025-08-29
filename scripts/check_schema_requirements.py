# scripts/check_schema_requirements.py
import json
from pathlib import Path

def check_schema_requirements():
    """Проверяет обязательные поля в схеме."""
    schema_path = Path("schemas/context-config/v1.5.schema.json")
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    
    # Проверяем требования к key_data
    key_data_properties = schema['properties']['key_data']['properties']
    required_fields = schema['properties']['key_data'].get('required', [])
    
    print("📋 Обязательные поля в key_data:")
    for field in required_fields:
        print(f"   - {field}")
    
    print("\n📋 Все свойства key_data:")
    for field, props in key_data_properties.items():
        required = " (ОБЯЗАТЕЛЬНО)" if field in required_fields else ""
        print(f"   - {field}: {props.get('type', 'unknown')}{required}")

if __name__ == "__main__":
    check_schema_requirements()