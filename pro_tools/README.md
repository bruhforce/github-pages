# Профессиональные инструменты для работы с языковыми моделями

Этот модуль представляет собой набор профессиональных инструментов для работы с языковыми моделями, включая управление промптами, версионирование и интеграцию с API.

## Возможности

- Создание и управление шаблонами промптов
- Версионирование промптов
- Интеграция с API различных языковых моделей
- Веб-интерфейс для тестирования промптов
- Интеграция с системой хранения диалогов

## Структура

- `api_clients/` - Клиенты для работы с API языковых моделей
- `prompt_manager/` - Система управления промптами
  - `prompt_templates/` - Шаблоны промптов
- `ui/` - Веб-интерфейс для работы с промптами
- `integration/` - Интеграция с системой хранения диалогов

## Использование

### Работа с API клиентами

```python
from pro_tools.api_clients.openai_client import OpenAIClient

# Инициализация клиента
client = OpenAIClient(api_key="ваш_api_ключ")  # или установите переменную окружения OPENAI_API_KEY

# Запрос на завершение текста
response = client.complete(
    prompt="Напишите рассказ о космическом путешествии",
    max_tokens=500
)

# Запрос в формате чата
chat_response = client.chat(
    messages=[
        {"role": "system", "content": "Вы - опытный писатель научной фантастики."},
        {"role": "user", "content": "Напишите начало рассказа о первом контакте с инопланетянами."}
    ]
)
```

### Работа с менеджером промптов

```python
from pro_tools.prompt_manager.prompt_versioning import PromptManager

# Инициализация менеджера промптов
manager = PromptManager()

# Создание шаблона промпта
template_id = manager.create_template(
    name="Генерация истории",
    template="Напишите {{length}} историю в жанре {{genre}} о {{subject}}.",
    description="Шаблон для генерации историй",
    variables=["length", "genre", "subject"]
)

# Рендеринг промпта с переменными
rendered_prompt = manager.render_prompt(
    template_id,
    variables={
        "length": "короткую",
        "genre": "научная фантастика",
        "subject": "первом контакте с инопланетянами"
    }
)
```

### Запуск веб-интерфейса

```bash
cd pro_tools/ui
python app.py
```

После запуска веб-интерфейс будет доступен по адресу http://localhost:5000

## Интеграция с системой диалогов

```python
from pro_tools.integration.context_bridge import ContextBridge

# Инициализация моста между системами
bridge = ContextBridge()

# Преобразование диалога в шаблон промпта
template_id = bridge.dialog_to_prompt_template(
    dialog_path="/path/to/dialog.md",
    template_name="Шаблон из диалога"
)

# Преобразование шаблона промпта в диалог
dialog_path = bridge.prompt_template_to_dialog(
    template_id=template_id,
    dialog_title="Диалог из шаблона"
)

# Тестирование промпта и сохранение результата как диалог
result = bridge.test_prompt_with_dialog(
    template_id=template_id,
    variables={"system_prompt": "Вы - помощник", "user_message": "Привет!"},
    dialog_title="Тестирование промпта"
)
```

## Требования

- Python 3.7+
- Установленные зависимости из requirements.txt
- API ключи для используемых языковых моделей

