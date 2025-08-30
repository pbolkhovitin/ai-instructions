# github_sync_example.py
import asyncio
from services.config_loader import load_from_local_or_github

async def sync_with_github():
    """Загружает最新нюю версию с GitHub, игнорируя локальную копию"""
    try:
        content = await load_from_local_or_github(
            local_path="configs/context_config_my-ai-project.json",
            github_relative_path="configs/context_config_my-ai-project.json"
        )
        print("✅ Успешная синхронизация с GitHub")
        return content
    except Exception as e:
        print(f"❌ Ошибка синхронизации: {e}")
        return None

asyncio.run(sync_with_github())