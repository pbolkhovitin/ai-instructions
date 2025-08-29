#!/usr/bin/env python3
"""
Скрипт для инициализации репозитория с базовой структурой.
Запустить: python scripts/initialize_repository.py
"""

import os
import json
from pathlib import Path

def create_repository_structure(base_path: str):
    """Создает базовую структуру репозитория."""
    directories = [
        'instructions',
        'schemas/deepseek-instructions',
        'schemas/context-config',
        'configs',
        'scripts'
    ]
    
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Создана директория: {dir_path}")
    
    # Создаем README.md
    readme_content = """# AI Instructions Repository

Репозиторий для хранения конфигураций, инструкций и схем валидации AI ассистента.

## Структура
- `instructions/` - базовые инструкции ассистента
- `schemas/` - JSON Schema для валидации
- `configs/` - конфиги контекста сессий
- `scripts/` - вспомогательные скрипты

## Использование
Ассистент автоматически загружает конфиги из этого репозитория с приоритетом локального клона.
"""
    
    readme_path = os.path.join(base_path, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Создан README.md: {readme_path}")

def create_gitignore(base_path: str):
    """Создает .gitignore файл."""
    gitignore_content = """# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# Temporary files
tmp/
temp/
"""
    
    gitignore_path = os.path.join(base_path, '.gitignore')
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print(f"Создан .gitignore: {gitignore_path}")

if __name__ == "__main__":
    base_path = "C:/Users/pbolk/Documents/GitHub/ai-instructions"
    
    print("Инициализация структуры репозитория...")
    create_repository_structure(base_path)
    create_gitignore(base_path)
    
    print("\nNext Steps:")
    print("1. Добавьте файлы в созданные директории")
    print("2. Инициализируйте git репозиторий:")
    print("   cd C:/Users/pbolk/Documents/GitHub/ai-instructions")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("3. Добавьте remote origin:")
    print("   git remote add origin https://github.com/pbolkhovitin/ai-instructions.git")
    print("4. Запушьте изменения:")
    print("   git push -u origin main")