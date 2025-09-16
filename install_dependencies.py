#!/usr/bin/env python3
"""
Автоматическая установка зависимостей из requirements.txt с логированием
"""

import subprocess
import sys
import os
import logging
import re
from datetime import datetime
from typing import List, Dict, Tuple

class DependencyInstaller:
    def __init__(self, requirements_file: str = "requirements.txt", log_file: str = "dependencies.log"):
        self.requirements_file = requirements_file
        self.log_file = log_file
        self.setup_logging()
        
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def read_requirements(self) -> List[str]:
        """Чтение зависимостей из файла"""
        try:
            if not os.path.exists(self.requirements_file):
                self.logger.error(f"Файл {self.requirements_file} не найден!")
                return []
            
            with open(self.requirements_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            dependencies = []
            for line in lines:
                line = line.strip()
                # Пропускаем пустые строки и комментарии
                if line and not line.startswith('#'):
                    dependencies.append(line)
            
            self.logger.info(f"Прочитано {len(dependencies)} зависимостей из {self.requirements_file}")
            return dependencies
            
        except Exception as e:
            self.logger.error(f"Ошибка чтения файла {self.requirements_file}: {e}")
            return []
    
    def check_package_installed(self, package: str) -> bool:
        """Проверка, установлен ли пакет"""
        try:
            # Извлекаем имя пакета без версии
            package_name = re.split(r'[>=<]', package)[0]
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package_name],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except Exception as e:
            self.logger.warning(f"Ошибка проверки пакета {package}: {e}")
            return False
    
    def install_dependency(self, dependency: str) -> Tuple[bool, str]:
        """Установка одной зависимости"""
        try:
            self.logger.info(f"Установка зависимости: {dependency}")
            
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", dependency],
                capture_output=True,
                text=True,
                check=True
            )
            
            self.logger.info(f"Успешно установлено: {dependency}")
            return True, result.stdout
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Ошибка установки {dependency}: {e.stderr}"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Неожиданная ошибка при установке {dependency}: {e}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def install_all_dependencies(self) -> Dict[str, dict]:
        """Установка всех зависимостей"""
        dependencies = self.read_requirements()
        if not dependencies:
            return {}
        
        self.logger.info("=" * 50)
        self.logger.info("НАЧАЛО УСТАНОВКИ ЗАВИСИМОСТЕЙ")
        self.logger.info("=" * 50)
        
        results = {}
        installed_count = 0
        skipped_count = 0
        failed_count = 0
        
        for dep in dependencies:
            if self.check_package_installed(dep):
                self.logger.info(f"Пакет уже установлен: {dep}")
                results[dep] = {"status": "skipped", "message": "Уже установлен"}
                skipped_count += 1
                continue
            
            success, message = self.install_dependency(dep)
            if success:
                results[dep] = {"status": "installed", "message": message}
                installed_count += 1
            else:
                results[dep] = {"status": "failed", "message": message}
                failed_count += 1
        
        # Сводка
        self.logger.info("=" * 50)
        self.logger.info("СВОДКА УСТАНОВКИ")
        self.logger.info("=" * 50)
        self.logger.info(f"Всего зависимостей: {len(dependencies)}")
        self.logger.info(f"Установлено: {installed_count}")
        self.logger.info(f"Пропущено (уже установлены): {skipped_count}")
        self.logger.info(f"Ошибок: {failed_count}")
        self.logger.info("=" * 50)
        
        return results
    
    def generate_report(self, results: Dict[str, dict]):
        """Генерация отчета"""
        report_file = "installation_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 📦 Отчёт установки зависимостей\n\n")
            f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Файл требований:** {self.requirements_file}\n\n")
            
            f.write("## Статистика\n")
            f.write(f"- Всего зависимостей: {len(results)}\n")
            installed = sum(1 for r in results.values() if r['status'] == 'installed')
            skipped = sum(1 for r in results.values() if r['status'] == 'skipped')
            failed = sum(1 for r in results.values() if r['status'] == 'failed')
            f.write(f"- Установлено: {installed}\n")
            f.write(f"- Пропущено: {skipped}\n")
            f.write(f"- Ошибок: {failed}\n\n")
            
            f.write("## Детализация\n")
            f.write("| Пакет | Статус | Сообщение |\n")
            f.write("|-------|--------|-----------|\n")
            
            for package, result in results.items():
                status_emoji = "✅" if result['status'] == 'installed' else "⚠️" if result['status'] == 'skipped' else "❌"
                f.write(f"| `{package}` | {status_emoji} {result['status']} | {result['message'][:100]}... |\n")
        
        self.logger.info(f"Отчёт сохранён в файл: {report_file}")

def main():
    """Основная функция"""
    installer = DependencyInstaller()
    
    # Проверяем существование requirements.txt
    if not os.path.exists(installer.requirements_file):
        installer.logger.error(f"Файл {installer.requirements_file} не найден!")
        sys.exit(1)
    
    # Устанавливаем зависимости
    results = installer.install_all_dependencies()
    
    # Генерируем отчет
    if results:
        installer.generate_report(results)
    
    # Проверяем наличие ошибок
    has_errors = any(result['status'] == 'failed' for result in results.values())
    if has_errors:
        installer.logger.error("Обнаружены ошибки при установке зависимостей!")
        sys.exit(1)
    else:
        installer.logger.info("Все зависимости успешно обработаны!")
        sys.exit(0)

if __name__ == "__main__":
    main()