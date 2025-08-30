# Файл: services/github_auth.py
import os
from typing import Optional

class GitHubAuth:
    """Менеджер аутентификации GitHub."""
    
    def __init__(self):
        self.token = self._get_token()
    
    def _get_token(self) -> Optional[str]:
        """Получает токен из переменных окружения или файла."""
        # 1. Переменная окружения (наиболее безопасно)
        token = os.environ.get('GITHUB_TOKEN')
        if token:
            return token
            
        # 2. Файл с токеном (для разработки)
        token_file = os.path.expanduser('~/.github_token')
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                return f.read().strip()
                
        return None
    
    def get_auth_headers(self) -> dict:
        """Возвращает заголовки для аутентификации."""
        if self.token:
            return {'Authorization': f'token {self.token}'}
        return {}