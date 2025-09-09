#!/usr/bin/env python3
"""
Скрипт детального аудита репозитория ai-instructions.
Анализирует содержимое директорий, включая вложенные структуры.
Формирует два файла отчета в корне проекта:
1. repo_structure_tree.txt - древовидная структура
2. repo_audit_report.txt - итоговый отчет
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import hashlib
from datetime import datetime

class RepoAuditor:
    """Класс для проведения детального аудита репозитория."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.tree_file = self.base_path / "repo_structure_tree.txt"
        self.report_file = self.base_path / "repo_audit_report.txt"
        self.results = {
            'directory_stats': {},
            'file_types': {},
            'json_validation': {},
            'duplicates': {},
            'schema_compliance': {},
            'issues': []
        }
        
        # Список игнорируемых папок и файлов (GitHub и технические)
        self.ignore_patterns = [
            '.git', '.github', '.vscode', '.venv', '__pycache__',
            'node_modules', '.DS_Store', 'Thumbs.db', '.idea'
        ]
    
    def should_ignore(self, item_name: str) -> bool:
        """Проверяет, нужно ли игнорировать файл/папку."""
        return any(pattern in item_name for pattern in self.ignore_patterns)
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Вычисляет MD5 хеш файла, пропускает симлинки."""
        try:
            # Пропускаем симлинки
            if file_path.is_symlink():
                return f"symlink_skip:{file_path.name}"
            
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            return f"error: {str(e)}"
    
    def validate_json(self, file_path: Path) -> Tuple[bool, Any]:
        """Проверяет валидность JSON файла."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            return True, content
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
    
    def check_schema_compliance(self, file_path: Path, content: Any) -> List[str]:
        """Проверяет базое соответствие ожидаемой структуре."""
        issues = []
        filename = file_path.name
        relative_path = str(file_path.relative_to(self.base_path))
        
        # Проверка для конфигурационных файлов
        if filename.startswith('context_config_') and filename.endswith('.json'):
            required_fields = ['meta', 'key_data', 'parent_settings']
            for field in required_fields:
                if field not in content:
                    issues.append(f"Missing required field: {field}")
            
            if 'meta' in content:
                meta_required = ['core_topic', 'conversation_style']
                for field in meta_required:
                    if field not in content['meta']:
                        issues.append(f"Missing meta field: {field}")
        
        # Проверка для файлов инструкций
        elif filename.startswith('deepseek_instructions_') and filename.endswith('.json'):
            required_fields = ['protocol_version', 'role', 'primary_goal', 'protocol']
            for field in required_fields:
                if field not in content:
                    issues.append(f"Missing required field: {field}")
        
        # Проверка для schema файлов
        elif 'schemas' in relative_path and filename.endswith('.schema.json'):
            schema_required = ['$schema', 'type', 'properties']
            for field in schema_required:
                if field not in content:
                    issues.append(f"Missing schema field: {field}")
        
        return issues
    
    def find_duplicates_ignore_symlinks(self, dir_path: Path) -> Dict[str, List[str]]:
        """
        Находит дубликаты файлов, игнорируя симлинки.
        
        Returns:
            Словарь {хеш: [список путей к файлам]}
        """
        hash_map = {}
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = Path(root) / file
                
                # Игнорируем симлинки и скрытые файлы
                if file_path.is_symlink() or self.should_ignore(file_path.name):
                    continue
                    
                try:
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash not in hash_map:
                        hash_map[file_hash] = []
                    hash_map[file_hash].append(str(file_path.relative_to(self.base_path)))
                except Exception as e:
                    print(f"Не удалось обработать файл {file_path}: {e}")
        
        # Возвращаем только настоящие дубликаты
        return {h: paths for h, paths in hash_map.items() if len(paths) > 1}

    def audit_directory_recursive(self, dir_path: Path, depth: int = 0) -> Dict[str, Any]:
        """Рекурсивно проводит аудит директории."""
        dir_stats = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'subdirectories': {},
            'files': [],
            'symlinks': []
        }
        
        hashes = {}
        
        try:
            for item in dir_path.iterdir():
                # Игнорируем скрытые файлы и папки
                if self.should_ignore(item.name):
                    continue
                    
                if item.is_file():
                    # Отдельно учитываем симлинки
                    if item.is_symlink():
                        dir_stats['symlinks'].append({
                            'name': item.name,
                            'target': os.readlink(item) if hasattr(os, 'readlink') else 'unknown',
                            'path': str(item.relative_to(self.base_path))
                        })
                        continue
                        
                    # Базовая статистика
                    file_size = item.stat().st_size
                    file_ext = item.suffix.lower()
                    
                    dir_stats['total_files'] += 1
                    dir_stats['total_size'] += file_size
                    dir_stats['file_types'][file_ext] = dir_stats['file_types'].get(file_ext, 0) + 1
                    
                    file_info = {
                        'name': item.name,
                        'size': file_size,
                        'extension': file_ext,
                        'path': str(item.relative_to(self.base_path)),
                        'is_symlink': item.is_symlink()
                    }
                    
                    # Валидация JSON файлов (только для не-симлинков)
                    if file_ext == '.json' and not item.is_symlink():
                        is_valid, validation_result = self.validate_json(item)
                        file_info['json_valid'] = is_valid
                        
                        if is_valid:
                            # Проверка соответствия схеме
                            schema_issues = self.check_schema_compliance(item, validation_result)
                            if schema_issues:
                                file_info['schema_issues'] = schema_issues
                                self.results['issues'].extend([
                                    f"{item.relative_to(self.base_path)}: {issue}" 
                                    for issue in schema_issues
                                ])
                        else:
                            file_info['json_error'] = validation_result
                            self.results['issues'].append(
                                f"{item.relative_to(self.base_path)}: {validation_result}"
                            )
                    
                    # Проверка на дубликаты (только для не-симлинков)
                    if not item.is_symlink():
                        file_hash = self.calculate_file_hash(item)
                        if file_hash.startswith('error:'):
                            file_info['hash_error'] = file_hash
                        else:
                            file_info['hash'] = file_hash
                            if file_hash in hashes:
                                if 'duplicates' not in self.results:
                                    self.results['duplicates'] = {}
                                self.results['duplicates'].setdefault(file_hash, []).append(
                                    str(item.relative_to(self.base_path))
                                )
                            hashes[file_hash] = str(item.relative_to(self.base_path))
                    
                    dir_stats['files'].append(file_info)
                
                elif item.is_dir() and depth < 5:  # Ограничиваем глубину рекурсии
                    subdir_name = item.name
                    dir_stats['subdirectories'][subdir_name] = self.audit_directory_recursive(item, depth + 1)
                    
                    # Суммируем статистику поддиректорий
                    subdir_stats = dir_stats['subdirectories'][subdir_name]
                    dir_stats['total_files'] += subdir_stats['total_files']
                    dir_stats['total_size'] += subdir_stats['total_size']
                    
                    for ext, count in subdir_stats['file_types'].items():
                        dir_stats['file_types'][ext] = dir_stats['file_types'].get(ext, 0) + count
        
        except PermissionError:
            print(f"   ⚠️  Нет доступа к директории: {dir_path}")
        
        return dir_stats
    
    def generate_tree_file(self):
        """Создает файл с древовидной структурой файлов и директорий."""
        print("🌳 Создание файла древовидной структуры...")
        
        with open(self.tree_file, 'w', encoding='utf-8') as tree_file:
            tree_file.write("=" * 60 + "\n")
            tree_file.write("ДРЕВОВИДНАЯ СТРУКТУРА РЕПОЗИТОРИЯ\n")
            tree_file.write("=" * 60 + "\n")
            tree_file.write(f"Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            tree_file.write(f"Корневая директория: {self.base_path}\n")
            tree_file.write(f"Игнорируемые паттерны: {', '.join(self.ignore_patterns)}\n\n")
            
            tree_file.write("СТРУКТУРА (игнорируются технические файлы):\n")
            tree_file.write("=" * 50 + "\n")
            self._write_tree_recursive(self.base_path, tree_file)
            
            tree_file.write(f"\nФайл создан: {self.tree_file}\n")
    
    def _write_tree_recursive(self, dir_path: Path, file_handle, prefix: str = ""):
        """Рекурсивно записывает дерево директорий в файл."""
        try:
            # Фильтруем элементы, исключая игнорируемые
            items = []
            for item in dir_path.iterdir():
                if not self.should_ignore(item.name):
                    items.append(item)
            
            items = sorted(items, key=lambda x: (not x.is_dir(), x.name))
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                
                if item.is_dir():
                    file_handle.write(f"{prefix}{connector}{item.name}/\n")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    self._write_tree_recursive(item, file_handle, new_prefix)
                else:
                    file_handle.write(f"{prefix}{connector}{item.name}\n")
        
        except PermissionError:
            file_handle.write(f"{prefix}└── [Нет доступа]\n")
    
    def run_audit(self) -> Dict[str, Any]:
        """Запускает полный аудит репозитория."""
        print("🔍 Запуск детального аудита репозитория...")
        print(f"📁 Корневая директория: {self.base_path}")
        
        # Создаем файл древовидной структуры
        self.generate_tree_file()
        print(f"✅ Файл структуры создан: {self.tree_file}")
        
        # Создаем файл отчета
        with open(self.report_file, 'w', encoding='utf-8') as report:
            report.write("=" * 60 + "\n")
            report.write("ИТОГОВЫЙ ОТЧЕТ АУДИТА РЕПОЗИТОРИЯ\n")
            report.write("=" * 60 + "\n")
            report.write(f"Дата аудита: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"Корневая директория: {self.base_path}\n")
            report.write(f"Игнорируемые паттерны: {', '.join(self.ignore_patterns)}\n\n")
        
        # Аудит каждой основной директории
        directories = [
            'instructions', 'configs', 'schemas', 
            'scripts', 'exports', 'backups'
        ]
        
        for dir_name in directories:
            dir_path = self.base_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                print(f"\n📂 АУДИТ ДИРЕКТОРИИ: {dir_name}/")
                self.results['directory_stats'][dir_name] = self.audit_directory_recursive(dir_path)
                
                stats = self.results['directory_stats'][dir_name]
                print(f"   Файлов: {stats['total_files']}")
                print(f"   Общий размер: {stats['total_size']} bytes")
                print(f"   Типы файлов: {stats['file_types']}")
        
        return self.results
    
    def generate_report(self):
        """Генерирует итоговый отчет в файл и выводит краткую информацию в консоль."""
        total_files = sum(stats['total_files'] for stats in self.results['directory_stats'].values())
        total_size = sum(stats['total_size'] for stats in self.results['directory_stats'].values())
        
        # Дописываем результаты в файл отчета
        with open(self.report_file, 'a', encoding='utf-8') as report:
            report.write("\n📈 ОБЩАЯ СТАТИСТИКА:\n")
            report.write(f"   Всего файлов: {total_files}\n")
            report.write(f"   Общий размер: {total_size} bytes\n")
            
            # Статистика по типам файлов
            all_file_types = {}
            for stats in self.results['directory_stats'].values():
                for ext, count in stats['file_types'].items():
                    all_file_types[ext] = all_file_types.get(ext, 0) + count
            
            report.write(f"   Типы файлов: {all_file_types}\n")
            
            # Детальная статистика по директориям
            report.write(f"\n📂 ДЕТАЛЬНАЯ СТАТИСТИКА ПО ДИРЕКТОРИЯМ:\n")
            for dir_name, stats in self.results['directory_stats'].items():
                report.write(f"   {dir_name}/: {stats['total_files']} файлов, {stats['total_size']} bytes\n")
            
            # Проблемы
            if self.results['issues']:
                report.write(f"\n❌ ОБНАРУЖЕННЫЕ ПРОБЛЕМЫ ({len(self.results['issues'])}):\n")
                for issue in self.results['issues']:
                    report.write(f"   - {issue}\n")
            else:
                report.write(f"\n✅ КРИТИЧЕСКИХ ПРОБЛЕМ НЕ ОБНАРУЖЕНО\n")
            
            # Дубликаты
            if self.results.get('duplicates'):
                report.write(f"\n⚠️  ОБНАРУЖЕНЫ ДУБЛИКАТЫ ФАЙЛОВ:\n")
                for hash_val, files in self.results['duplicates'].items():
                    report.write(f"   Хеш {hash_val[:8]}...:\n")
                    for file_path in files:
                        report.write(f"     - {file_path}\n")
            else:
                report.write(f"\n✅ ДУБЛИКАТЫ НЕ ОБНАРУЖЕНЫ\n")
            
            report.write(f"\n📋 Файлы отчетов:\n")
            report.write(f"   • Древовидная структура: {self.tree_file.name}\n")
            report.write(f"   • Итоговый отчет: {self.report_file.name}\n")
        
        # Краткий вывод в консоль
        print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        print(f"   Всего файлов: {total_files}")
        print(f"   Общий размер: {total_size} bytes")
        
        issues_count = len(self.results['issues'])
        if issues_count > 0:
            print(f"   ❌ Проблем: {issues_count}")
        else:
            print(f"   ✅ Критических проблем не обнаружено")
        
        duplicates_count = len(self.results.get('duplicates', {}))
        if duplicates_count > 0:
            print(f"   ⚠️  Дубликатов: {duplicates_count}")
        else:
            print(f"   ✅ Дубликатов не обнаружено")
        
        print(f"\n📄 Файлы отчетов созданы:")
        print(f"   • {self.tree_file}")
        print(f"   • {self.report_file}")

def main():
    """Основная функция скрипта."""
    repo_path = "C:/Users/pbolk/Documents/GitHub/ai-instructions"
    
    if not os.path.exists(repo_path):
        print(f"❌ Репозиторий не найден по пути: {repo_path}")
        sys.exit(1)
    
    auditor = RepoAuditor(repo_path)
    results = auditor.run_audit()
    auditor.generate_report()
    
    if results['issues']:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()