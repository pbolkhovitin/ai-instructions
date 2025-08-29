#!/usr/bin/env python3
"""
Скрипт для проверки корректности структуры схем.
"""

from pathlib import Path

def verify_schemas_structure():
    repo_path = Path("C:/Users/pbolk/Documents/GitHub/ai-instructions")
    schemas_dir = repo_path / "schemas"
    
    print("🔍 Проверка структуры схем...")
    
    # Проверяем обязательные элементы
    checks = [
        (schemas_dir / "index.json", "Индексный файл"),
        (schemas_dir / "deepseek-instructions" / "latest.schema.json", "Симлинк инструкций"),
        (schemas_dir / "context-config" / "latest.schema.json", "Симлинк конфигов"),
        (schemas_dir / "README.md", "Документация"),
    ]
    
    all_ok = True
    for path, description in checks:
        if path.exists():
            print(f"✅ {description}: существует")
        else:
            print(f"❌ {description}: отсутствует")
            all_ok = False
    
    return all_ok

if __name__ == "__main__":
    success = verify_schemas_structure()
    sys.exit(0 if success else 1)