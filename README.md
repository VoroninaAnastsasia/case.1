# Text Analyzer

 Описание

Сервис для анализа текста: определение языка, тональности, субъективности, читаемости (Flesch Reading Ease), лексического разнообразия и плотности редких слов.

Возможности

- Определение языка: русский, английский, немецкий, французский.
- Анализ тональности: позитивная, нейтральная, негативная.
- Субъективность текста от 0 до 100 процентов.
- Индекс Флеша (Flesch Reading Ease) и интерпретация.
- Индекс Флеша-Кинкейда (Flesch-Kincaid Grade Level).
- Лексическое разнообразие и плотность редких слов.
- Кэширование результатов через Redis.
- Пакетная обработка массива текстов.
- REST API на FastAPI с автодокументацией Swagger.
- CLI на Click с командой analyze.
- Веб-интерфейс на HTML и JavaScript.

Стек технологий

- Python 3.11+
- FastAPI и Uvicorn
- Pydantic
- Redis
- TextBlob, LangDetect, Deep-Translator
- pytest, coverage
- locust

Установка

Выполните команды:

pip install -r requirements.txt
python -m textblob.download_corpora

Запуск

Запустите веб-сервер командой:

python main.py

Сервер запустится на http://127.0.0.1:8000

- Веб-интерфейс: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs

# CLI

Примеры команд:

python interfaces/cli.py analyze --text "This is a simple test."
python interfaces/cli.py analyze --file text.txt
python interfaces/cli.py analyze --batch-file texts.txt

# API

POST /analyze — анализ одного текста.

Запрос:
{"text": "This is a simple test."}

POST /analyze-batch — анализ массива текстов.

Запрос:
{"texts": ["First text.", "Second text."]}

# Тесты

Запуск тестов с покрытием:

pytest --cov=. --cov-report=term-missing

Требуемое покрытие — не менее 80 процентов.

# Нагрузочное тестирование

Запуск Locust:

locust -f locustfile.py --host=http://127.0.0.1:8000

Откройте http://localhost:8089 в браузере.

# Docker

Запуск через Docker Compose:

docker-compose up

# Структура проекта

case.1/
  application/     — сценарии использования
  domain/          — типы данных
  infrastructure/  — реализации
  interfaces/      — API и CLI
  static/          — веб-интерфейс
  tests/           — тесты
  main.py          — точка входа FastAPI
  Dockerfile       — сборка контейнера
  requirements.txt — зависимости
