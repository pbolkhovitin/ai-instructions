#!/usr/bin/env python3
"""
Скрипт для проверки структуры репозитория ai-instructions.
Проверяет наличие обязательных директорий и файлов.
"""

import os
import sys
from pathlib import Path

def check_repo_structure(base_path):
    """
    Проверяет структуру репозитория.
    
    Args:
        base_path (str): Путь к корню репозитория.
    
    Returns:
        dict: Результаты проверки {путь: существует}.
    """
    base_dir = Path(base_path)
    
    # Ожидаемая структура директорий
    expected_dirs = [
        base_dir / "instructions",    # Основные файлы инструкций
        base_dir / "configs",         # Конфигурационные файлы
        base_dir / "schemas",         # Схемы данных
        base_dir / "scripts",         # Вспомогательные скрипты
        base_dir / "exports",         # Экспортированные дампы
        base_dir / "backups",         # Резервные копии
    ]
    
    # Ожидаемые файлы (опциональные, но желательные)
    expected_files = [
        base_dir / "README.md",
        base_dir / ".gitignore",
    ]
    
    results = {}
    
    print("🔍 Проверка структуры репозитория...")
    print(f"📁 Корневая директория: {base_dir}")
    print("\n" + "="*50)
    
    # Проверяем директории
    print("\n📂 ПРОВЕРКА ДИРЕКТОРИЙ:")
    for dir_path in expected_dirs:
        exists = dir_path.exists() and dir_path.is_dir()
        results[str(dir_path)] = exists
        status = "✅ СУЩЕСТВУЕТ" if exists else "❌ ОТСУТСТВУЕТ"
        print(f"{status} {dir_path.relative_to(base_dir)}")
    
    # Проверяем файлы
    print("\n📄 ПРОВЕРКА ФАЙЛОВ:")
    for file_path in expected_files:
        exists = file_path.exists() and file_path.is_file()
        results[str(file_path)] = exists
        status = "✅ СУЩЕСТВУЕТ" if exists else "⚠️  ОТСУТСТВУЕТ"
        print(f"{status} {file_path.relative_to(base_dir)}")
    
    # Дополнительная информация о существующих директориях
    print("\n📊 ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")
    for dir_path in expected_dirs:
        if dir_path.exists() and dir_path.is_dir():
            items = list(dir_path.iterdir())
            print(f"   {dir_path.relative_to(base_dir)}/ ({len(items)} элементов)")
            for item in items[:5]:  # Показываем первые 5 элементов
                print(f"     - {item.name}")
            if len(items) > 5:
                print(f"     ... и еще {len(items) - 5}")
    
    return results

def main():
    """Основная функция скрипта."""
    # Определяем путь к репозиторию
    repo_path = "C:/Users/pbolk/Documents/GitHub/ai-instructions"
    
    if not os.path.exists(repo_path):
        print(f"❌ Репозиторий не найден по пути: {repo_path}")
        print("Пожалуйста, укажите правильный путь к репозиторию.")
        sys.exit(1)
    
    # Проверяем структуру
    results = check_repo_structure(repo_path)
    
    # Сводка
    print("\n" + "="*50)
    total_checked = len(results)
    total_passed = sum(1 for exists in results.values() if exists)
    
    print(f"\n📈 СВОДКА: {total_passed}/{total_checked} проверок пройдено")
    
    if total_passed == total_checked:
        print("🎉 Структура репозитория соответствует ожиданиям!")
    else:
        print("⚠️  Обнаружены отклонения от ожидаемой структуры.")
        print("\nРекомендуемые действия:")
        print("1. Создайте отсутствующие директории")
        print("2. Добавьте README.md с описанием репозитория")
        print("3. Настройте .gitignore для исключения временных файлов")

if __name__ == "__main__":
    main()