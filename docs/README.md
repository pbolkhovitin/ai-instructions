# Документация проекта AI Instructions

Данная документация описывает структуру, использование и поддержку репозитория инструкций для онлайн-версий ИИ.

## 📋 Обзор

Проект содержит оптимизированные протоколы взаимодействия с ИИ-ассистентами, сфокусированные на актуальных версиях:

1. **DeepSeek Protocol v4.1.0** – для модели DeepSeek-V4 с семантическим версионированием, модульной архитектурой и 1M контекстом.
2. **ChatGPT Protocol v1.9.3** – модульная система инструкций для ChatGPT (GPT-5) с расширенными возможностями.
3. **Grok Core Protocol v4.0** – оптимизированный протокол для Grok (xAI) с системой персон.

## 🏗️ Структура проекта

```
ai-instructions/
├── instructions/                   # ИНСТРУКЦИИ ДЛЯ ИИ
│   ├── deepseek_v4/               # DeepSeek Protocol v4.1.0 (актуально)
│   │   ├── core_protocol_v4.1.0.json       # Ядро протокола
│   │   ├── think_pipeline_v4.1.0.json       # 7-шаговый анализ
│   │   ├── memory_management_v4.1.0.json   # Управление памятью
│   │   ├── advanced_analytics_v4.1.0.json  # Аналитика и метрики
│   │   ├── file_operations_v4.1.0.json     # Работа с файлами
│   │   ├── web_search_v4.1.0.json          # Интернет-поиск
│   │   ├── cross_validation_v4.1.0.json    # Перекрёстная валидация
│   │   ├── topic_fork_v4.1.0.json          # Вынос тем (форки)
│   │   ├── system_documentation_v4.1.0.json
│   │   ├── detailed_descriptions_v4.1.0.json
│   │   ├── troubleshooting_guide_v4.1.0.json
│   │   ├── command_examples_v4.1.0.json
│   │   ├── validation_schemas_v4.1.0.json
│   │   ├── version_manifest_v4.1.0.json    # Манифест версий
│   │   ├── core_protocol_v4.0.json         # (legacy, до 2026-06-08)
│   │   └── README_RUS_v4.0.md
│   ├── chatgpt/                   # ChatGPT Protocol v1.9.3 (актуально)
│   │   ├── assistant_instructions_v1.9.3-chatgpt.json
│   │   ├── assistant_extensions_v1.9.2.json
│   │   ├── assistant_specialized_modules_v1.9.3.json
│   │   ├── assistant_memory_protocol.json
│   │   ├── assistant_config_template_v1.9.2.json
│   │   └── README_RUS.md
│   ├── grock/                     # Grok Core Protocol v4.0 (актуально)
│   │   ├── grok_core_protocol_v4.0_full.json
│   │   └── README_RUS_v4.0.md
│   └── deepseek_instructions_latest.json -> deepseek_v4/core_protocol_v4.1.0.json
├── configs/                       # КОНФИГУРАЦИИ КОНТЕКСТА
│   ├── context_config_v1.9.json
│   └── github_config.json
├── schemas/                       # СХЕМЫ ВАЛИДАЦИИ JSON
│   ├── context-config/
│   │   ├── v1.9.schema.json
│   │   └── latest.schema.json -> v1.9.schema.json
│   ├── deepseek-instructions/
│   │   ├── v1.9.schema.json
│   │   └── latest.schema.json -> v1.9.schema.json
│   ├── selective-export/
│   ├── return-export/
│   └── index.json
├── scripts/                       # ВСПОМОГАТЕЛЬНЫЕ СКРИПТЫ
│   ├── validate_config.py
│   ├── repo_audit.py
│   ├── generate_schemas_index.py
│   └── github_sync.py
├── services/                      # СЕРВИСНЫЕ МОДУЛИ (Python)
│   ├── config_loader.py
│   └── schema_manager.py
├── docs/                          # ДОКУМЕНТАЦИЯ
│   ├── README.md
│   └── migration_v4.0_to_v4.1.md  # Гайд миграции
├── tests/                         # ТЕСТЫ
└── plans/                         # ПЛАНЫ И ОТЧЕТЫ
    └── audit_report.md
```

## 🚀 Использование

### DeepSeek Protocol v4.1.0

1. **Инициализация (новый формат):**
```
[ПРОТОКОЛ: ЗАГРУЗИТЬ] https://raw.githubusercontent.com/pbolkhovitin/ai-instructions/main/instructions/deepseek_v4/core_protocol_v4.1.0.json [ПАРАМЕТРЫ: persona=A, user_name=Имя]
```

2. **Дополнительные модули:** При необходимости загрузите другие JSON-файлы через `[МОДУЛИ: ЗАГРУЗИТЬ ...]`.

3. **Команды:**
   - `[ЗАГРУЗИТЬ: файл.pdf]` – загрузить документ
   - `[ПОИСК: запрос]` – поиск в интернете
   - `[ВЕРДИКТ: СТАТУС]` – проверить состояние контекста
   - `[CRAFT: ФАЙЛЫ]` – оптимизировать работу с файлами

Подробнее в `instructions/deepseek_v4/README_RUS_v4.0.md`.

**Миграция с v4.0:** [migration_v4.0_to_v4.1.md](migration_v4.0_to_v4.1.md)

### ChatGPT Protocol v1.9.3

1. **Загрузка:** Используйте `assistant_instructions_v1.9.3-chatgpt.json` как инструкции ассистента в ChatGPT.
2. **Модули:** Система автоматически определит наличие дополнительных модулей и загрузит их.
3. **Расширения:** Функциональные расширения добавляют визуальную обработку, анализ данных, интернет-поиск.

Подробнее в `instructions/chatgpt/README_RUS.md`.

### Grok Core Protocol v4.0

1. **Загрузка:** Используйте `grok_core_protocol_v4.0_full.json` как системное сообщение Grok.
2. **Персона:** Система предложит выбор персоны (A/B/C) при старте.
3. **Think Pipeline:** Работает при включенном "Режиме мышления".

## ⚙️ Поддержка и валидация

### Валидация конфигов
```bash
python scripts/validate_config.py configs/context_config_v1.9.json
```

### Аудит репозитория
```bash
python scripts/repo_audit.py
```

### Обновление индекса схем
```bash
python scripts/generate_schemas_index.py
```

## 🔄 Планы развития

1. **Обновление схем** – создание схем v4.1.0 для DeepSeek Protocol.
2. **Конфигурация v4.1** – разработка `context_config_v4.1.json`.
3. **Интеграция с CI/CD** – автоматическая валидация при коммитах.
4. **Расширение документации** – добавление руководств по использованию каждого модуля.

## 📝 Лицензия

© Pavel Bolkhovitin, 2025–2026. Все права защищены.
Конфигурации и протоколы являются коммерческой тайной.

**Версия документации:** 2026-05-08
**Актуальные протоколы:** DeepSeek v4.1.0, ChatGPT v1.9.3, Grok v4.0
