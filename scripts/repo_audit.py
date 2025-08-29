#!/usr/bin/env python3
"""
Скрипт детального аудита репозитория ai-instructions.
Анализирует содержимое директорий, включая вложенные структуры.
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import hashlib

class RepoAuditor:
    """Класс для проведения детального аудита репозитория."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.results = {
            'directory_stats': {},
            'file_types': {},
            'json_validation': {},
            'duplicates': {},
            'schema_compliance': {},
            'issues': []
        }
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Вычисляет MD5 хеш файла."""
        try:
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
        """Проверяет базовое соответствие ожидаемой структуре."""
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
    
    def audit_directory_recursive(self, dir_path: Path, depth: int = 0) -> Dict[str, Any]:
        """Рекурсивно проводит аудит директории."""
        dir_stats = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'subdirectories': {},
            'files': []
        }
        
        hashes = {}
        
        try:
            for item in dir_path.iterdir():
                if item.is_file():
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
                        'path': str(item.relative_to(self.base_path))
                    }
                    
                    # Валидация JSON файлов
                    if file_ext == '.json':
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
                    
                    # Проверка на дубликаты
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
    
    def print_directory_tree(self, dir_path: Path, prefix: str = ""):
        """Выводит дерево директорий с файлами."""
        try:
            items = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                
                if item.is_dir():
                    print(f"{prefix}{connector}{item.name}/")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    self.print_directory_tree(item, new_prefix)
                else:
                    print(f"{prefix}{connector}{item.name}")
        
        except PermissionError:
            print(f"{prefix}└── [Нет доступа]")
    
    def run_audit(self) -> Dict[str, Any]:
        """Запускает полный аудит репозитория."""
        print("🔍 Запуск детального аудита репозитория...")
        print(f"📁 Корневая директория: {self.base_path}")
        
        # Выводим дерево структуры
        print("\n🌳 СТРУКТУРА РЕПОЗИТОРИЯ:")
        self.print_directory_tree(self.base_path)
        
        print("\n" + "="*60)
        
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
                print(f"   Файлов: {stats['total_files']} (включая поддиректории)")
                print(f"   Общий размер: {stats['total_size']} bytes")
                print(f"   Типы файлов: {stats['file_types']}")
                
                # Показываем JSON issues если есть
                self._print_json_issues(stats)
        
        return self.results
    
    def _print_json_issues(self, stats):
        """Рекурсивно выводит проблемы JSON файлов."""
        for file_info in stats.get('files', []):
            if file_info['extension'] == '.json':
                if not file_info.get('json_valid', True):
                    print(f"   ❌ {file_info['path']}: {file_info.get('json_error', 'Unknown error')}")
                elif file_info.get('schema_issues'):
                    print(f"   ⚠️  {file_info['path']}: {len(file_info['schema_issues'])} schema issues")
        
        for subdir_stats in stats.get('subdirectories', {}).values():
            self._print_json_issues(subdir_stats)
    
    def generate_report(self):
        """Генерирует итоговый отчет."""
        print("\n" + "="*60)
        print("📊 ИТОГОВЫЙ ОТЧЕТ АУДИТА")
        print("="*60)
        
        total_files = sum(stats['total_files'] for stats in self.results['directory_stats'].values())
        total_size = sum(stats['total_size'] for stats in self.results['directory_stats'].values())
        
        print(f"\n📈 ОБЩАЯ СТАТИСТИКА:")
        print(f"   Всего файлов: {total_files}")
        print(f"   Общий размер: {total_size} bytes")
        print(f"   Типы файлов: {self.results['file_types']}")
        
        # Детальная статистика по директориям
        print(f"\n📂 ДЕТАЛЬНАЯ СТАТИСТИКА ПО ДИРЕКТОРИЯМ:")
        for dir_name, stats in self.results['directory_stats'].items():
            print(f"   {dir_name}/: {stats['total_files']} файлов, {stats['total_size']} bytes")
        
        # Проблемы
        if self.results['issues']:
            print(f"\n❌ ОБНАРУЖЕННЫЕ ПРОБЛЕМЫ ({len(self.results['issues'])}):")
            for issue in self.results['issues'][:10]:
                print(f"   - {issue}")
            if len(self.results['issues']) > 10:
                print(f"   ... и еще {len(self.results['issues']) - 10} проблем")
        else:
            print(f"\n✅ КРИТИЧЕСКИХ ПРОБЛЕМ НЕ ОБНАРУЖЕНО")
        
        # Дубликаты
        if self.results.get('duplicates'):
            print(f"\n⚠️  ОБНАРУЖЕНЫ ДУБЛИКАТЫ ФАЙЛОВ:")
            for hash_val, files in self.results['duplicates'].items():
                print(f"   Хеш {hash_val[:8]}...:")
                for file_path in files:
                    print(f"     - {file_path}")
        else:
            print(f"\n✅ ДУБЛИКАТЫ НЕ ОБНАРУЖЕНЫ")

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