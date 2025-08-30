# Файл: services/github_utils.py
"""
Утилиты для работы с GitHub API и URL конструкцией.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
from .github_auth import GitHubAuth

class GitHubURLConstructor:
    """Конструктор URL для GitHub API и RAW доступа."""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_github_config(config_path)
        self.auth = GitHubAuth()
    
    def _load_github_config(self, config_path: str = None) -> Dict[str, Any]:
        """Загружает конфигурацию GitHub из файла или использует значения по умолчанию."""
        default_config = {
            "api_base": "https://api.github.com",
            "raw_base": "https://raw.githubusercontent.com",
            "repo_owner": "pbolkhovitin",
            "repo_name": "ai-instructions", 
            "branch": "main"
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    return {**default_config, **user_config.get('github', {})}
            except Exception as e:
                print(f"⚠️  Ошибка загрузки конфига GitHub: {e}. Использую значения по умолчанию.")
        
        return default_config
    
    def get_raw_url(self, relative_path: str) -> str:
        """Генерирует URL для GitHub RAW."""
        relative_path = relative_path.lstrip('/')
        return f"{self.config['raw_base']}/{self.config['repo_owner']}/{self.config['repo_name']}/{self.config['branch']}/{relative_path}"
    
    def get_api_url(self, endpoint: str) -> str:
        """Генерирует URL для GitHub API."""
        endpoint = endpoint.lstrip('/')
        return f"{self.config['api_base']}/repos/{self.config['repo_owner']}/{self.config['repo_name']}/{endpoint}"
    
    def get_contents_url(self, path: str = "") -> str:
        """Генерирует URL для GitHub Contents API."""
        return self.get_api_url(f"contents/{path}")
    
    def get_headers(self) -> Dict[str, str]:
        """Возвращает заголовки для запросов с аутентификацией."""
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'AI-Instructions-Loader'
        }
        headers.update(self.auth.get_auth_headers())
        return headers

# Глобальный экземпляр для удобства
github_urls = GitHubURLConstructor()

# Функции для быстрого доступа
def get_raw_url(relative_path: str) -> str:
    """Быстрое получение RAW URL."""
    return github_urls.get_raw_url(relative_path)

def get_api_url(endpoint: str) -> str:
    """Быстрое получение API URL."""
    return github_urls.get_api_url(endpoint)

def get_auth_headers() -> Dict[str, str]:
    """Быстрое получение заголовков с аутентификацией."""
    return github_urls.get_headers()