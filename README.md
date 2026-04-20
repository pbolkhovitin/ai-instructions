# AI Instructions Repository

Репозиторий для хранения инструкций, конфигураций и схем валидации для онлайн-версий ИИ (DeepSeek, ChatGPT и других). Основное содержимое — оптимизированные протоколы взаимодействия с ИИ-ассистентами.

## 🎯 Актуальные версии

### DeepSeek Protocol v3.0
**Оптимизирован для DeepSeek-V3** с поддержкой 1M контекста, работы с файлами (50+ форматов) и интернет-поиска.

**Ключевые возможности:**
- Полное управление контекстом 1M токенов
- Работа с файлами: PDF, DOCX, Excel, код, изображения (через OCR)
- Интернет-поиск с верификацией источников
- Модульная архитектура: ядро, управление памятью, аналитика
- Интеграция с Obsidian для визуализации диалогов
- Защита интеллектуальной собственности (RBAC, обфускация)

**Директория:** `instructions/deepseek_v3/`

### ChatGPT Protocol v1.9.3
**Многоуровневая система инструкций для ChatGPT (GPT-5)** с модульной архитектурой.

**Ключевые возможности:**
- Стадийная загрузка модулей (базовый протокол → расширения → специализированные модули)
- Поддержка визуальной обработки, анализа данных, интернет-поиска
- Расширенный модуль памяти: долговременные, проектные и временные знания
- Голосовые ответы и внешние интеграции

**Директория:** `instructions/chatgpt/`

## 📁 Структура проекта (актуальная)

```
ai-instructions/
├── instructions/                   # ИНСТРУКЦИИ ДЛЯ ИИ
│   ├── deepseek_v3/               # DeepSeek Protocol v3.0 (актуально)
│   │   ├── core_protocol_v3.0.json
│   │   ├── memory_management_v3.0.json
│   │   ├── advanced_analytics_v3.0.json
│   │   ├── file_operations_v3.0.json
│   │   ├── web_search_v3.0.json
│   │   └── README_RUS_v3.0.md
│   ├── chatgpt/                   # ChatGPT Protocol v1.9.3 (актуально)
│   │   ├── assistant_instructions_v1.9.3-chatgpt.json
│   │   ├── assistant_extensions_v1.9.2.json
│   │   ├── assistant_specialized_modules_v1.9.3.json
│   │   ├── assistant_memory_protocol.json
│   │   ├── assistant_config_template_v1.9.2.json
│   │   └── README_RUS.md
│   └── deepseek_instructions_latest.json -> deepseek_v3/core_protocol_v3.0.json (симлинк)
├── configs/                       # КОНФИГУРАЦИИ КОНТЕКСТА
│   ├── context_config_v1.9.json   # Актуальный конфиг (требует обновления до v3.0)
│   └── github_config.json         # Конфигурация GitHub (токен должен быть в .env)
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
│   ├── validate_config.py         # Валидация конфигов по схемам
│   ├── repo_audit.py              # Аудит структуры репозитория
│   ├── generate_schemas_index.py  # Генерация индекса схем
│   └── github_sync.py             # Синхронизация с GitHub
├── services/                      # СЕРВИСНЫЕ МОДУЛИ (Python)
│   ├── config_loader.py           # Загрузчик конфигов с валидацией
│   └── schema_manager.py          # Менеджер JSON-схем
├── docs/                          # ДОКУМЕНТАЦИЯ
│   └── README.md
├── tests/                         # ТЕСТЫ
├── plans/                         # ПЛАНЫ И ОТЧЕТЫ
│   └── audit_report.md            # Отчет аудита (2026-04-20)
└── .codeassistant/                # КОНФИГУРАЦИЯ CODE ASSISTANT
```

## ⚙️ Быстрый старт

### Использование DeepSeek v3.0
1. Скопируйте содержимое `instructions/deepseek_v3/core_protocol_v3.0.json` в системное сообщение DeepSeek-V3.
2. Загрузите дополнительные модули по необходимости:
   - `memory_management_v3.0.json` — управление памятью
   - `file_operations_v3.0.json` — работа с файлами
   - `web_search_v3.0.json` — интернет-поиск
3. Используйте команды протокола:
   ```
   [ЗАГРУЗИТЬ: файл.pdf]      # Загрузить документ
   [ПОИСК: запрос]            # Поиск в интернете
   [ВЕРДИКТ: СТАТУС]          # Проверить состояние контекста
   ```

### Использование ChatGPT v1.9.3
1. Загрузите `assistant_instructions_v1.9.3-chatgpt.json` как инструкции ассистента в ChatGPT.
2. Система автоматически определит наличие дополнительных модулей и загрузит их.
3. Используйте команды модулей для расширенной функциональности.

## 🔄 Обновление проекта

Проект находится в процессе аудита и очистки. Устаревшие версии (DeepSeek v1.9.0, v1.9.2, v2.0; Grok; Alice; GigaChat) будут удалены или перемещены в архив.

**Текущий статус:** Проведен аудит, составлен [план очистки](plans/audit_report.md).

## 📝 Лицензия

© Pavel Bolkhovitin, 2025–2026. Все права защищены.
Конфигурации и протоколы являются коммерческой тайной.

**Версия документации:** 2026-04-20  
**Актуальные протоколы:** DeepSeek v3.0, ChatGPT v1.9.3