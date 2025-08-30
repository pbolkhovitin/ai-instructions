# check_github_access.py
from services.github_auth import GitHubAuth
from services.github_utils import get_raw_url, get_auth_headers

def check_github_access():
    auth = GitHubAuth()
    
    print("🔍 Проверка доступа к GitHub:")
    print(f"Токен доступен: {auth.has_token()}")
    print(f"Режим доступа: {'Приватный' if auth.has_token() else 'Публичный'}")
    
    # Пример URL
    test_url = get_raw_url("instructions/deepseek_instructions_v1.5.json")
    print(f"Пример GitHub URL: {test_url}")
    
    # Заголовки аутентификации
    headers = get_auth_headers()
    print(f"Заголовки запроса: {headers}")

check_github_access()