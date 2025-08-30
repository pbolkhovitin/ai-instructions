# Файл: tests/create_simple_test.py
import json
import os

# Создаем минимальный валидный конфиг для теста
test_config = {
    "config_version": "1.5.1",
    "protocol_version": "1.5",
    "role": "Тестовый ассистент",
    "style": "технический",
    "primary_goal": "Тестирование валидации",
    "emphasis": "Тестирование",
    "protocol": {
        "memory_management": {
            "proactive_summarization": {
                "triggers": ["тест"],
                "summary_format": "--- Тест ---"
            },
            "context_monitoring": {
                "verdicts": {
                    "OPTIMAL": {"condition": "тест", "description": "тест", "label": "тест"},
                    "WORKING": {"condition": "тест", "description": "тест", "label": "тест"}
                },
                "requirement": "тест"
            }
        }
    },
    "commands": {
        "format": ["тест"],
        "tasks": ["тест"],
        "analysis": ["тест"],
        "system": ["тест"],
        "control": ["тест"]
    },
    "principles": {
        "proactivity": "тест",
        "structure": "тест", 
        "honesty": "тест",
        "efficiency": "test"
    },
    "confirmation": "тест"
}

# Сохраняем в instructions директорию
os.makedirs('instructions', exist_ok=True)
test_file = 'instructions/deepseek_instructions_v1.5.json'

with open(test_file, 'w', encoding='utf-8') as f:
    json.dump(test_config, f, indent=2, ensure_ascii=False)

print(f"✅ Тестовый конфиг создан: {test_file}")