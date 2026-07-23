# Developer CV AI Backend API
Асинхронный REST API сервис на FastAPI, разработанный для обработки формы обратной связи персонального сайта разработчика. Сервис анализирует входящие обращения с помощью GigaChat API, выполняет строгое валидирование данных, рассылает email-уведомления, фиксирует метрики в JSON и защищен от спама.


## Технологический стек
* Фреймворк: FastAPI (0.139.2) + Uvicorn (0.51.0)
* Валидация: Pydantic (2.13.4) & Pydantic Settings (2.14.2)
* LLM / ИИ: GigaChat SDK (0.2.1)
* Email рассылка: fastapi-mail (1.6.5) + aiosmtplib (5.1.2)
* Rate Limiting: slowapi (0.1.10)
* Логирование: loguru (0.7.3)
* Тестирование: pytest (9.1.1) + pytest-asyncio (1.4.0)

## Как запустить проект
### 1. Клонирование репозитория и создание окружения
```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd developer-cv-ai-backend

# Создание виртуального окружения
python -m venv .venv

# Активация окружения (Windows)
.venv\Scripts\activate

# Активация окружения (Linux/macOS)
source .venv/bin/activate
```
### 2. Создайте и активируйте виртуальное окружение:
Windows:
```bash
python -m venv .venv
.venv\Scripts\activatesh
```
Linux / macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Установка зависимостей
```bash
pip install -r src\requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл .env в корневой директории проекта со следующим содержимым:
```ini
APP_NAME="Developer CV API"
DEBUG=True
PORT=8000

# CORS
CORS_ORIGINS="http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000"

# GigaChat API Credentials
GIGACHAT_CREDENTIALS="ваш_client_secret_gigachat"
GIGACHAT_SCOPE="GIGACHAT_API_PERS"

# SMTP Настройки (Яндекс / Mail.ru / Gmail)
MAIL_USERNAME="your-email@yandex.ru"
MAIL_PASSWORD="your-app-password"
MAIL_FROM="your-email@yandex.ru"
MAIL_PORT=465
MAIL_SERVER="smtp.yandex.ru"
MAIL_FROM_NAME="Developer CV Site"
ADMIN_EMAIL="your-email@yandex.ru"

# Rate Limiting
RATE_LIMIT_CONTACT="5/minute"
```
### 4. Запустите сервер разработки
```bash
python -m src.app.main
```
Или через Uvicorn:
```bash
uvicorn src.app.main:app --reload
```
После запуска документация и сервисы доступны по адресам:
* Swagger UI (Interactive API): http://127.0.0.1:8000/docs
* ReDoc Documentation: http://127.0.0.1:8000/redoc

## Архитектура проекта
### 1. Структура проекта
```text
developer-cv-ai-backend/
├── src/
│   └── app/
│       ├── api/
│       │   └── v1/
│       │       ├── endpoints/
│       │       │   ├── contact.py      # Роут POST /api/contact
│       │       │   └── metrics.py      # Роуты GET и /metrics
│       │       └── routers.py          # Объединенный API v1 роутер
│       ├── core/
│       │   ├── config.py               # Pydantic Settings конфигурация
│       │   ├── exceptions.py           # Глобальный обработчик ошибок
│       │   ├── limiter.py              # Настройка SlowAPI (Rate limit)
│       │   └── logging.py              # Настройка Loguru
│       ├── data/
│       │   └── stats.json              # Файл хранения статистики обращений
│       ├── logs/
│       ├── schemas/
│       │   └── contact.py              # Pydantic-модели валидации
│       ├── services/
│       │   ├── ai_services.py          # Логика работы с GigaChat
│       │   ├── email_service.py        # Отправка писем через FastMail
│       │   └── stats_service.py        # Чтение и обновление метрик
│       ├── storage/
│       │   └── logs/
│       │       └── app.log             # Файлы логов приложения
│       ├── __init__.py
│       └── main.py                     # Точка входа в приложение
├── .env.example                        # Пример переменных окружения
├── .gitignore                          # Исключения Git
├── README.md                           # Документация проекта
└── requirements.txt                    # Зависимости
```
### 2. Паттерны проектирования
Паттерны проектирования
1. Singleton (Одиночка): Сервисы AIService, EmailService, StatsService и объект limiter создаются в единичном экземпляре при старте модуля.
2. Repository / Storage Pattern: Изолированная работа с JSON-файлом статистики в классах-сервисах.
3. Modular Application / Router: Разделение роутов на версионированные модули (api/v1/...).
4. Graceful Fallback: Паттерн гарантированной деградации функционала при отказе внешнего AI-сервиса.

### 3. Объяснение выбора технологий
Объяснение выбора технологий
* FastAPI: Выбран из-за нативной поддержки асинхронности (Async/Await), высокой скорости и авто-генерации Swagger docs.
* GigaChat: Оптимальная русскоязычная LLM, официально доступная из РФ без сетевых задержек и VPN.
* Loguru: Значительно проще и информативнее стандартного logging, нативно поддерживает асинхронность и ротацию.

## 4. Реализация API
Описание эндпоинтов
* POST `/api/contact` — Отправка формы обратной связи.
* GET `/api/metrics` — Получение агрегированной статистики и метрик обращений.
* GET / — Автоматический редирект на `/docs`.

### Примеры запросов и ответов
POST `/api/contact`
Запрос (Request Body):
```json
{
  "name": "Алексей",
  "email": "alexey@example.com",
  "phone": "+79991234567",
  "comments": "Здравствуйте! Хотим предложить вам участие в проекте."
}
```
Успешный ответ (200 OK):
```json
{
  "status": "success",
  "message": "Ваше обращение успешно обработано!"
}
```
GET `/api/metrics`
Ответ (200 OK):
```json
{
  "status": "success",
  "data": {
    "total_requests": 5,
    "categories": {
      "collaboration": 3,
      "question": 2
    },
    "sentiments": {
      "neutral": 4,
      "positive": 1
    }
  }
}
```

### алидация и обработка ошибок
Pydantic Валидация (ContactFormRequest):
* `name`: от 1 до 50 символов.
* `email`: строгая проверка EmailStr.
* `phone`: кастомный field_validator очищает строки от пробелов/скобок и проверяет регулярным выражением ^\+?[0-9]{10,15}$.
* `comments`: от 5 до 2000 символов.

Единый обработчик ошибок (setup_exception_handlers):
`422 Unprocessable Entity` — Ошибка валидации данных с детальным описанием полей.
`429 Too Many Requests` — Превышение лимита запросов (Rate Limit).
`500 Internal Server Error` — Критические сбои без утечки чувствительной информации наружу.

## 5. AI-интеграция
### AI-инструменты и назначение
Используется GigaChat API через официальный Python SDK.
Назначение:
* Определение тональности сообщения (sentiment: positive, neutral, negative).
* Классификация обращения (category: job_offer, question, collaboration, other).
* Автоматическая генерация персонализированного ответа посетителю.

### Реализация Fallback (Graceful Degradation)
Если ключ `GIGACHAT_CREDENTIALS` не задан, превышены квоты API или сервис Сбера недоступен:
Метод `ai_service.analyze_and_respond(...)` перехватывает исключение через try-except.
Возвращается безопасный резервный ответ (`get_feelback_responce`), выставляющий метку `"is_fallback": True`.
Сервис продолжит работу, отправит письма и сохранит статистику без генерации ошибки 500 для пользователя.

### Используемые Промпты
Системный промпт (System Prompt):
```text
Ты — AI-ассистент на личном сайте разработчика. Проанализируй сообщение от посетителя и сформируй ответ.
Верни ответ СТРОГО в формате JSON без разметки markdown и без дополнительного текста со следующими полями:
1. 'sentiment': тональность ('positive', 'neutral', 'negative')
2. 'category': тип запроса ('job_offer', 'question', 'collaboration', 'other')
3. 'auto_reply': вежливый и короткий авто-ответ на русском языке (2-3 предложения).
```
Пользовательский промпт (User Prompt):
```text
Имя отправителя: {name}
Сообщение: {comments}
```

## 6. Что сделано с помощью AI 
### Какие части кода генерировались:
1. Шаблонная обвязка FastAPI и pydantic-конфиги (config.py, limiter.py).
2. Логика отправки писем fastapi-mail (email_service.py).
3. Регулярное выражение для валидации номеров телефонов.
4. Юнит-тесты на pytest.
### Какие промпты использовались:
1. "Напиши асинхронный сервис на FastAPI с интеграцией GigaChat, отправкой писем через fastapi-mail и ограничением запросов slowapi."
2. "Создай pydantic-схему для валидации номера телефона, убирающую скобки и тире."
### Что пришлось исправлять вручную:
1. SMTP Настройки Яндекса: Выявление ошибки авторизации 535 5.7.8, переключение протоколов почтовых программ в Yandex ID и перевод на порт 465 (MAIL_SSL_TLS=True).
2. Обработка ответа GigaChat: Ручной парсинг сырой строки с помощью регулярных выражений `(re.search(r"\{.*\}", ...))`, так как LLM иногда добавляла лишние текстовые блоки или символы переноса, вызавая ошибку json.loads (Extra data).
3. FastAPI Lifespan: Заменен устаревший декоратор `@app.on_event("startup")` на современный контекстный менеджер lifespan.
4. Дублирование логов: Добавлена очистка стандартных обработчиков `logger.remove()` перед настройкой Loguru.

## 7. Хранение данных
### Хранение логов
1. Логи записываются с помощью библиотеки Loguru.
2. Форматированные логи консоли выводятся в sys.stdout.
3. Логи сохраняются в файл `storage/logs/app.log` с автоматической ротацией при достижении 5 MB и хранением за последние 10 дней (в архиве .zip).

### Rate Limiting (Защита от спама)
1. Реализован с помощью библиотеки `SlowAPI` (аналог Flask-Limiter).
2. Ограничение задается декоратором `@limiter.limit("5/minute")` на эндпоинте `/api/contact`.
3. Идентификация пользователя происходит по IP-адресу (`get_remote_address`).
4. При превышении порога возвращается статус-код 429 Too Many Requests.

### Хранение статистики
1. Статистика хранится в локальном файле `data/stats.json`.
2. Класс `StatsService` потокобезопасно (в рамках асинхронного процесса) считывает, инкрементирует и атомарно перезаписывает данные по категориям и тональности при каждом обращении.
