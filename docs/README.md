# Документация проекта AI Instructions

Данная документация описывает структуру, использование и поддержку репозитория инструкций для онлайн-версий ИИ.

## 📋 Обзор

Проект содержит оптимизированные протоколы взаимодействия с ИИ-ассистентами, сфокусированные на двух актуальных версиях:

1. **DeepSeek Protocol v3.0** – для модели DeepSeek-V3 с поддержкой 1M контекста, работы с файлами и интернет-поиска.
2. **ChatGPT Protocol v1.9.3** – модульная система инструкций для ChatGPT (GPT-5) с расширенными возможностями.

Остальные версии (DeepSeek v1.9.0, v1.9.2, v2.0; Grok; Alice; GigaChat) были удалены в ходе аудита 2026-04-20.

## 🏗️ Структура проекта (после очистки)

```
ai-instructions/
├── instructions/                   # ИНСТРУКЦИИ ДЛЯ ИИ
│   ├── deepseek_v3/               # DeepSeek Protocol v3.0 (актуально)
│   │   ├── core_protocol_v3.0.json          # Ядро протокола
│   │   ├── memory_management_v3.0.json      # Управление памятью
│   │   ├── advanced_analytics_v3.0.json     # Аналитика и метрики
│   │   ├── file_operations_v3.0.json        # Работа с файлами
│   │   ├── web_search_v3.0.json             # Интернет-поиск
│   │   ├── cross_validation_v3.0.json       # Перекрёстная валидация
│   │   ├── topic_fork_v3.0.json             # Вынос тем (форки)
│   │   ├── system_documentation_v3.0.json   # Документация системы
│   │   ├── detailed_descriptions_v3.0.json  # Детальные описания
│   │   ├── troubleshooting_guide_v3.0.json  # Решение проблем
│   │   ├── command_examples_v3.0.json       # Примеры команд
│   │   ├── validation_schemas_v3.0.json     # Схемы валидации
│   │   └── README_RUS_v3.0.md               # Описание версии
│   ├── chatgpt/                   # ChatGPT Protocol v1.9.3 (актуально)
│   │   ├── assistant_instructions_v1.9.3-chatgpt.json    # Базовый протокол
│   │   ├── assistant_extensions_v1.9.2.json              # Функциональные расширения
│   │   ├── assistant_specialized_modules_v1.9.3.json     # Специализированные модули
│   │   ├── assistant_memory_protocol.json                # Расширенный модуль памяти
│   │   ├── assistant_config_template_v1.9.2.json         # Конфигурация проекта
│   │   └── README_RUS.md                                 # Описание версии
│   └── deepseek_instructions_latest.json    # Копия core_protocol_v3.0.json (удобная ссылка)
├── configs/                       # КОНФИГУРАЦИИ КОНТЕКСТА
│   ├── context_config_v1.9.json   # Актуальный конфиг (требует обновления до v3.0)
│   └── github_config.json         # Конфигурация GitHub (токен должен быть в .env)
├── schemas/                       # СХЕМЫ ВАЛИДАЦИИ JSON
│   ├── context-config/            # Схемы для конфигов контекста
│   │   ├── v1.9.schema.json
│   │   └── latest.schema.json -> v1.9.schema.json
│   ├── deepseek-instructions/     # Схемы для инструкций DeepSeek
│   │   ├── v1.9.schema.json       # Устарела, требует обновления до v3.0
│   │   └── latest.schema.json -> v1.9.schema.json
│   ├── selective-export/          # Схемы выборочного экспорта
│   ├── return-export/             # Схемы возврата результатов
│   └── index.json                 # Автоматически генерируемый индекс
├── scripts/                       # ВСПОМОГАТЕЛЬНЫЕ СКРИПТЫ
│   ├── validate_config.py         # Валидация конфигов по схемам
│   ├── repo_audit.py              # Аудит структуры репозитория
│   ├── generate_schemas_index.py  # Генерация индекса схем
│   ├── github_sync.py             # Синхронизация с GitHub
│   └── ... (другие утилиты)
├── services/                      # СЕРВИСНЫЕ МОДУЛИ (Python)
│   ├── config_loader.py           # Загрузчик конфигов с валидацией
│   └── schema_manager.py          # Менеджер JSON-схем
├── docs/                          # ДОКУМЕНТАЦИЯ (этот файл)
├── tests/                         # ТЕСТЫ
├── plans/                         # ПЛАНЫ И ОТЧЕТЫ
│   └── audit_report.md            # Отчет аудита (2026-04-20)
└── .codeassistant/                # КОНФИГУРАЦИЯ CODE ASSISTANT
```

## 🚀 Использование

### DeepSeek Protocol v3.0

1. **Быстрый старт**: Скопируйте содержимое `instructions/deepseek_v3/core_protocol_v3.0.json` в системное сообщение DeepSeek-V3.
2. **Дополнительные модули**: При необходимости загрузите другие JSON-файлы из той же директории (память, файлы, поиск и т.д.).
3. **Команды**: Используйте команды протокола, например:
   - `[ЗАГРУЗИТЬ: файл.pdf]` – загрузить документ
   - `[ПОИСК: запрос]` – поиск в интернете
   - `[ВЕРДИКТ: СТАТУС]` – проверить состояние контекста
   - `[CRAFT: ФАЙЛЫ]` – оптимизировать работу с файлами

Подробнее в `instructions/deepseek_v3/README_RUS_v3.0.md`.

### ChatGPT Protocol v1.9.3

1. **Загрузка**: Используйте `assistant_instructions_v1.9.3-chatgpt.json` как инструкции ассистента в ChatGPT.
2. **Модули**: Система автоматически определит наличие дополнительных модулей и загрузит их.
3. **Расширения**: Функциональные расширения добавляют визуальную обработку, анализ данных, интернет-поиск.

Подробнее в `instructions/chatgpt/README_RUS.md`.

## ⚙️ Поддержка и валидация

### Валидация конфигов
Запустите скрипт для проверки соответствия схеме:
```bash
python scripts/validate_config.py configs/context_config_v1.9.json
```

### Аудит репозитория
Для проверки структуры и выявления проблем:
```bash
python scripts/repo_audit.py
```

### Обновление индекса схем
После добавления новых схем:
```bash
python scripts/generate_schemas_index.py
```

## 🔄 Планы развития

1. **Обновление схем** – создание схем v3.0 для DeepSeek Protocol.
2. **Конфигурация v3.0** – разработка `context_config_v3.0.json`.
3. **Интеграция с CI/CD** – автоматическая валидация при коммитах.
4. **Расширение документации** – добавление руководств по использованию каждого модуля.

Текущий статус задач отслеживается в `plans/audit_report.md`.

## 📝 Лицензия

© Pavel Bolkhovitin, 2025–2026. Все права защищены.
Конфигурации и протоколы являются коммерческой тайной.

**Версия документации:** 2026-04-20  
**Актуальные протоколы:** DeepSeek v3.0, ChatGPT v1.9.3