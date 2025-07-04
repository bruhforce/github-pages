# Разветвление диалогов в промпт-инженерии

![[branching_dialogs.png]]

## 📚 Содержание

- [[#Введение]]
- [[#Что такое разветвление диалогов]]
- [[#Почему это важно]]
- [[#Методы разветвления диалогов]]
  - [[#Метод 1: Сохранение контекста в текстовых файлах]]
  - [[#Метод 2: Использование специализированных инструментов]]
  - [[#Метод 3: Локальные решения с открытым исходным кодом]]
  - [[#Метод 4: Профессиональные платформы]]
- [[#Практические примеры]]
  - [[#Пример 1: Разветвление с помощью текстовых файлов]]
  - [[#Пример 2: Разветвление с помощью ChatGPT]]
  - [[#Пример 3: Разветвление с помощью Python и LangChain]]
- [[#Лучшие практики]]
- [[#Ресурсы для дальнейшего изучения]]

## Введение

Промпт-инженерия — это искусство и наука создания эффективных запросов (промптов) для языковых моделей. Одна из ключевых задач промпт-инженера — тестирование различных вариантов промптов и анализ результатов. Для этого часто требуется **разветвление диалогов** — возможность продолжить диалог с моделью с одной точки в нескольких разных направлениях.

В этом руководстве мы рассмотрим практические методы разветвления диалогов, которые помогут вам эффективно тестировать и оптимизировать ваши промпты.

## Что такое разветвление диалогов

**Разветвление диалогов** — это техника, позволяющая сохранить определенное состояние диалога с языковой моделью и продолжить его в нескольких разных направлениях. Это похоже на создание точки сохранения в видеоигре, к которой вы можете вернуться, чтобы исследовать разные пути.

![[dialog_branching_concept.png]]

## Почему это важно

Разветвление диалогов критически важно для промпт-инженеров по нескольким причинам:

1. **Эффективность тестирования** — позволяет быстро сравнивать результаты разных промптов без необходимости повторять весь диалог
2. **Систематический анализ** — помогает методично исследовать пространство возможных промптов
3. **Оптимизация промптов** — упрощает итеративное улучшение промптов на основе результатов
4. **Документирование процесса** — облегчает сохранение истории экспериментов и их результатов

## Методы разветвления диалогов

### Метод 1: Сохранение контекста в текстовых файлах

Самый простой и доступный метод — сохранение полного контекста диалога в текстовых файлах.

#### Пошаговая инструкция:

1. **Создайте базовый шаблон** с системным промптом и начальными сообщениями
2. **Сохраните контрольную точку** диалога в текстовый файл после достижения интересующего вас состояния
3. **Создайте копии** этого файла для каждого варианта разветвления
4. **Добавьте разные продолжения** в каждую копию
5. **Используйте эти файлы** для продолжения диалога с моделью

#### Пример структуры файла:

```markdown
# Контрольная точка: Анализ данных

## Системный промпт
Ты — опытный аналитик данных, помогающий интерпретировать результаты исследования.

## Диалог
Пользователь: У меня есть данные о продажах за последний квартал. Как мне их проанализировать?

Ассистент: Я могу помочь вам с анализом данных о продажах. Для начала, какие конкретные аспекты вас интересуют? Например:
1. Общие тренды продаж
2. Сравнение с предыдущими периодами
3. Анализ по категориям продуктов
4. Региональный анализ
5. Анализ сезонности

Пользователь: Меня интересуют общие тренды и сравнение с предыдущим кварталом.

## Разветвление 1: Запрос дополнительных данных
Ассистент: Для анализа общих трендов и сравнения с предыдущим кварталом мне потребуются следующие данные:
...

## Разветвление 2: Предложение методологии
Ассистент: Для анализа общих трендов и сравнения с предыдущим кварталом я рекомендую следующую методологию:
...
```

### Метод 2: Использование специализированных инструментов

Многие современные интерфейсы для работы с языковыми моделями предлагают встроенные функции для разветвления диалогов.

#### ChatGPT Advanced Data Analysis (бывший Code Interpreter)

1. **Начните диалог** в ChatGPT с включенным режимом Advanced Data Analysis
2. **Дойдите до точки**, где хотите создать разветвление
3. **Используйте функцию "Continue this conversation in a new chat"** (доступна через меню "..." рядом с сообщением)
4. **Создайте несколько продолжений** из одной и той же точки
5. **Сравните результаты** разных ветвей

#### Claude Sonnet и Anthropic Console

1. **Начните диалог** с Claude
2. **Используйте функцию "Save checkpoint"** в интерфейсе Anthropic Console
3. **Создайте новые сессии** из сохраненной контрольной точки
4. **Продолжите диалог** в разных направлениях

### Метод 3: Локальные решения с открытым исходным кодом

Для более гибкого контроля над процессом разветвления можно использовать библиотеки с открытым исходным кодом.

#### Использование LangChain для разветвления диалогов

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Инициализация модели
chat = ChatOpenAI(temperature=0)

# Базовый диалог
base_messages = [
    SystemMessage(content="Ты — опытный аналитик данных."),
    HumanMessage(content="У меня есть данные о продажах за последний квартал. Как мне их проанализировать?"),
    AIMessage(content="Я могу помочь вам с анализом данных о продажах. Какие конкретные аспекты вас интересуют?"),
    HumanMessage(content="Меня интересуют общие тренды и сравнение с предыдущим кварталом.")
]

# Сохранение контрольной точки
checkpoint = base_messages.copy()

# Разветвление 1: Запрос дополнительных данных
branch1 = checkpoint.copy()
branch1.append(HumanMessage(content="Какие данные мне нужно подготовить для анализа?"))
response1 = chat(branch1)
branch1.append(response1)
print("Ветвь 1:", response1.content)

# Разветвление 2: Предложение методологии
branch2 = checkpoint.copy()
branch2.append(HumanMessage(content="Какую методологию анализа вы рекомендуете?"))
response2 = chat(branch2)
branch2.append(response2)
print("Ветвь 2:", response2.content)
```

#### Создание простого интерфейса с Streamlit

```python
import streamlit as st
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Инициализация модели
chat = ChatOpenAI(temperature=0)

# Функция для преобразования сообщений в формат LangChain
def convert_to_langchain_messages(messages):
    result = []
    for msg in messages:
        if msg["role"] == "system":
            result.append(SystemMessage(content=msg["content"]))
        elif msg["role"] == "user":
            result.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            result.append(AIMessage(content=msg["content"]))
    return result

# Инициализация состояния сессии
if "checkpoints" not in st.session_state:
    st.session_state.checkpoints = {}
if "current_messages" not in st.session_state:
    st.session_state.current_messages = [
        {"role": "system", "content": "Ты — опытный аналитик данных."}
    ]

# Интерфейс
st.title("Инструмент разветвления диалогов")

# Отображение текущего диалога
for msg in st.session_state.current_messages:
    if msg["role"] == "system":
        st.info(f"Системный промпт: {msg['content']}")
    elif msg["role"] == "user":
        st.write(f"Пользователь: {msg['content']}")
    elif msg["role"] == "assistant":
        st.write(f"Ассистент: {msg['content']}")

# Ввод нового сообщения
user_input = st.text_area("Ваше сообщение:")
if st.button("Отправить"):
    # Добавление сообщения пользователя
    st.session_state.current_messages.append({"role": "user", "content": user_input})
    
    # Получение ответа от модели
    langchain_messages = convert_to_langchain_messages(st.session_state.current_messages)
    response = chat(langchain_messages)
    
    # Добавление ответа ассистента
    st.session_state.current_messages.append({"role": "assistant", "content": response.content})
    st.experimental_rerun()

# Создание контрольной точки
checkpoint_name = st.text_input("Название контрольной точки:")
if st.button("Сохранить контрольную точку"):
    st.session_state.checkpoints[checkpoint_name] = st.session_state.current_messages.copy()
    st.success(f"Контрольная точка '{checkpoint_name}' сохранена!")

# Загрузка контрольной точки
if st.session_state.checkpoints:
    selected_checkpoint = st.selectbox("Выберите контрольную точку:", list(st.session_state.checkpoints.keys()))
    if st.button("Загрузить контрольную точку"):
        st.session_state.current_messages = st.session_state.checkpoints[selected_checkpoint].copy()
        st.experimental_rerun()

# Экспорт/импорт контрольных точек
if st.button("Экспорт контрольных точек"):
    export_data = json.dumps(st.session_state.checkpoints)
    st.download_button("Скачать контрольные точки", export_data, "checkpoints.json")

uploaded_file = st.file_uploader("Импорт контрольных точек", type="json")
if uploaded_file is not None:
    import_data = json.load(uploaded_file)
    st.session_state.checkpoints.update(import_data)
    st.success("Контрольные точки импортированы!")
```

### Метод 4: Профессиональные платформы

Для серьезной работы над промптами существуют специализированные платформы.

#### Humanloop

1. **Создайте проект** в Humanloop
2. **Определите базовый промпт** и параметры модели
3. **Создайте несколько вариантов** промпта
4. **Запустите эксперимент** для сравнения результатов
5. **Анализируйте метрики** для выбора лучшего варианта

#### Weights & Biases (W&B)

1. **Инициализируйте проект** в W&B
2. **Интегрируйте код** для логирования промптов и ответов
3. **Запустите эксперименты** с разными вариантами промптов
4. **Визуализируйте результаты** для сравнения эффективности

```python
import wandb
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Инициализация W&B
wandb.init(project="prompt-engineering-branching")

# Инициализация модели
chat = ChatOpenAI(temperature=0)

# Базовый диалог
base_messages = [
    SystemMessage(content="Ты — опытный аналитик данных."),
    HumanMessage(content="У меня есть данные о продажах за последний квартал. Как мне их проанализировать?"),
    AIMessage(content="Я могу помочь вам с анализом данных о продажах. Какие конкретные аспекты вас интересуют?"),
    HumanMessage(content="Меня интересуют общие тренды и сравнение с предыдущим кварталом.")
]

# Логирование базового диалога
wandb.log({
    "base_dialog": [{"role": m.__class__.__name__, "content": m.content} for m in base_messages]
})

# Разветвление 1: Запрос дополнительных данных
branch1 = base_messages.copy()
branch1.append(HumanMessage(content="Какие данные мне нужно подготовить для анализа?"))
response1 = chat(branch1)
branch1.append(response1)

# Логирование первого разветвления
wandb.log({
    "branch1_prompt": "Какие данные мне нужно подготовить для анализа?",
    "branch1_response": response1.content
})

# Разветвление 2: Предложение методологии
branch2 = base_messages.copy()
branch2.append(HumanMessage(content="Какую методологию анализа вы рекомендуете?"))
response2 = chat(branch2)
branch2.append(response2)

# Логирование второго разветвления
wandb.log({
    "branch2_prompt": "Какую методологию анализа вы рекомендуете?",
    "branch2_response": response2.content
})

# Завершение эксперимента
wandb.finish()
```

## Практические примеры

### Пример 1: Разветвление с помощью текстовых файлов

Рассмотрим пример разработки промпта для генерации маркетингового текста.

**Шаг 1:** Создайте базовый файл `marketing_prompt_base.txt`:

```
# Контрольная точка: Маркетинговый текст

## Системный промпт
Ты — опытный маркетолог, специализирующийся на создании убедительных рекламных текстов.

## Диалог
Пользователь: Мне нужен маркетинговый текст для нового приложения для медитации. Оно называется "ZenMind" и помогает пользователям снизить стресс и улучшить концентрацию.

Ассистент: Я помогу вам создать убедительный маркетинговый текст для вашего приложения для медитации "ZenMind". Чтобы текст был максимально эффективным, мне нужно знать:
1. Кто ваша целевая аудитория?
2. Какие основные функции приложения?
3. Чем ваше приложение отличается от конкурентов?
4. Какой тон и стиль вы предпочитаете (формальный, дружелюбный, вдохновляющий)?

Пользователь: Целевая аудитория — занятые профессионалы 25-45 лет, которые испытывают стресс на работе. Основные функции: короткие медитации (5-15 минут), отслеживание прогресса, напоминания и персонализированные рекомендации. Отличие от конкурентов — фокус на коротких сессиях и интеграция с рабочим календарем. Стиль — профессиональный, но дружелюбный.
```

**Шаг 2:** Создайте разветвление 1 в файле `marketing_prompt_branch1.txt` (эмоциональный подход):

```
# Контрольная точка: Маркетинговый текст - Эмоциональный подход

## Системный промпт
Ты — опытный маркетолог, специализирующийся на создании убедительных рекламных текстов.

## Диалог
Пользователь: Мне нужен маркетинговый текст для нового приложения для медитации. Оно называется "ZenMind" и помогает пользователям снизить стресс и улучшить концентрацию.

Ассистент: Я помогу вам создать убедительный маркетинговый текст для вашего приложения для медитации "ZenMind". Чтобы текст был максимально эффективным, мне нужно знать:
1. Кто ваша целевая аудитория?
2. Какие основные функции приложения?
3. Чем ваше приложение отличается от конкурентов?
4. Какой тон и стиль вы предпочитаете (формальный, дружелюбный, вдохновляющий)?

Пользователь: Целевая аудитория — занятые профессионалы 25-45 лет, которые испытывают стресс на работе. Основные функции: короткие медитации (5-15 минут), отслеживание прогресса, напоминания и персонализированные рекомендации. Отличие от конкурентов — фокус на коротких сессиях и интеграция с рабочим календарем. Стиль — профессиональный, но дружелюбный.

Пользователь: Создай текст, который фокусируется на эмоциональных преимуществах и чувстве облегчения, которое получат пользователи.
```

**Шаг 3:** Создайте разветвление 2 в файле `marketing_prompt_branch2.txt` (практический подход):

```
# Контрольная точка: Маркетинговый текст - Практический подход

## Системный промпт
Ты — опытный маркетолог, специализирующийся на создании убедительных рекламных текстов.

## Диалог
Пользователь: Мне нужен маркетинговый текст для нового приложения для медитации. Оно называется "ZenMind" и помогает пользователям снизить стресс и улучшить концентрацию.

Ассистент: Я помогу вам создать убедительный маркетинговый текст для вашего приложения для медитации "ZenMind". Чтобы текст был максимально эффективным, мне нужно знать:
1. Кто ваша целевая аудитория?
2. Какие основные функции приложения?
3. Чем ваше приложение отличается от конкурентов?
4. Какой тон и стиль вы предпочитаете (формальный, дружелюбный, вдохновляющий)?

Пользователь: Целевая аудитория — занятые профессионалы 25-45 лет, которые испытывают стресс на работе. Основные функции: короткие медитации (5-15 минут), отслеживание прогресса, напоминания и персонализированные рекомендации. Отличие от конкурентов — фокус на коротких сессиях и интеграция с рабочим календарем. Стиль — профессиональный, но дружелюбный.

Пользователь: Создай текст, который подчеркивает практические преимущества и экономию времени для занятых профессионалов.
```

**Шаг 4:** Используйте эти файлы для получения и сравнения результатов от языковой модели.

### Пример 2: Разветвление с помощью ChatGPT

1. **Начните диалог** с системным промптом:
   ```
   Ты — опытный UX-дизайнер, помогающий разработать интерфейс мобильного приложения.
   ```

2. **Опишите задачу**:
   ```
   Я разрабатываю приложение для отслеживания привычек. Мне нужны рекомендации по дизайну главного экрана.
   ```

3. **Уточните детали**:
   ```
   Целевая аудитория — молодые профессионалы 20-35 лет. Основные функции: добавление привычек, отслеживание прогресса, напоминания и статистика.
   ```

4. **Создайте новый чат** с тем же контекстом и запросите фокус на минималистичном дизайне:
   ```
   Предложи концепцию минималистичного дизайна главного экрана с фокусом на простоту использования.
   ```

5. **Создайте еще один чат** с тем же контекстом и запросите фокус на геймификации:
   ```
   Предложи концепцию дизайна главного экрана с элементами геймификации для повышения мотивации пользователей.
   ```

6. **Сравните результаты** разных подходов и выберите наиболее подходящий или объедините лучшие идеи.

### Пример 3: Разветвление с помощью Python и LangChain

```python
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import json

# Настройка API ключа
os.environ["OPENAI_API_KEY"] = "ваш_api_ключ"

# Инициализация модели
chat = ChatOpenAI(temperature=0.7)

# Функция для сохранения диалога в JSON
def save_dialog(messages, filename):
    serialized = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            serialized.append({"role": "system", "content": msg.content})
        elif isinstance(msg, HumanMessage):
            serialized.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            serialized.append({"role": "assistant", "content": msg.content})
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(serialized, f, ensure_ascii=False, indent=2)

# Функция для загрузки диалога из JSON
def load_dialog(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        serialized = json.load(f)
    
    messages = []
    for msg in serialized:
        if msg["role"] == "system":
            messages.append(SystemMessage(content=msg["content"]))
        elif msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    
    return messages

# Базовый диалог
base_messages = [
    SystemMessage(content="Ты — опытный копирайтер, специализирующийся на создании заголовков для статей."),
    HumanMessage(content="Мне нужен заголовок для статьи о преимуществах удаленной работы."),
]

# Получение ответа от модели
response = chat(base_messages)
base_messages.append(response)

# Добавление уточнения
base_messages.append(HumanMessage(content="Статья ориентирована на руководителей компаний, которые рассматривают возможность перехода на гибридный формат работы."))
response = chat(base_messages)
base_messages.append(response)

# Сохранение контрольной точки
save_dialog(base_messages, "headline_checkpoint.json")
print("Контрольная точка сохранена!")

# Разветвление 1: Формальный стиль
branch1 = load_dialog("headline_checkpoint.json")
branch1.append(HumanMessage(content="Сделай заголовок более формальным и ориентированным на бизнес-результаты."))
response1 = chat(branch1)
branch1.append(response1)
save_dialog(branch1, "headline_formal.json")
print("Разветвление 1 (формальный стиль):", response1.content)

# Разветвление 2: Провокационный стиль
branch2 = load_dialog("headline_checkpoint.json")
branch2.append(HumanMessage(content="Сделай заголовок более провокационным, чтобы привлечь внимание."))
response2 = chat(branch2)
branch2.append(response2)
save_dialog(branch2, "headline_provocative.json")
print("Разветвление 2 (провокационный стиль):", response2.content)

# Разветвление 3: Ориентация на данные
branch3 = load_dialog("headline_checkpoint.json")
branch3.append(HumanMessage(content="Включи в заголовок упоминание статистики или данных."))
response3 = chat(branch3)
branch3.append(response3)
save_dialog(branch3, "headline_data_driven.json")
print("Разветвление 3 (ориентация на данные):", response3.content)
```

## Лучшие практики

1. **Документируйте контрольные точки** — всегда добавляйте описание и метаданные к сохраненным контрольным точкам
2. **Используйте систематический подход** — планируйте разветвления заранее, а не создавайте их хаотично
3. **Сравнивайте результаты объективно** — определите критерии оценки до начала экспериментов
4. **Итерируйте постепенно** — вносите небольшие изменения между разветвлениями для лучшего понимания влияния каждого изменения
5. **Комбинируйте лучшие элементы** — используйте результаты разных ветвей для создания оптимального промпта
6. **Автоматизируйте рутинные операции** — создавайте скрипты для часто выполняемых действий
7. **Используйте версионирование** — присваивайте версии вашим промптам для отслеживания эволюции

## Ресурсы для дальнейшего изучения

- [[Prompt Engineering Guide|https://www.promptingguide.ai/]] — подробное руководство по промпт-инженерии
- [[LangChain Documentation|https://python.langchain.com/]] — документация по библиотеке LangChain
- [[Humanloop Documentation|https://docs.humanloop.com/]] — руководство по платформе Humanloop
- [[Weights & Biases Documentation|https://docs.wandb.ai/]] — документация по W&B
- [[Promptfoo|https://github.com/promptfoo/promptfoo]] — инструмент для тестирования и оценки промптов
- [[LangSmith|https://smith.langchain.com/]] — платформа для отладки и оптимизации LLM-приложений

---

*Создано с помощью Manus AI для демонстрации работы с GitHub репозиторием.*

