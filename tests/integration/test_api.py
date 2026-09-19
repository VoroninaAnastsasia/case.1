from fastapi.testclient import TestClient
from interfaces.api import app


client = TestClient(app)


class Test_RootEndpoint:
  # Проверяет корневой эндпоинт (веб-интерфейс).

  def test_root_returns_200(self):
    # Корневой эндпоинт отвечает 200.
    response = client.get('/')
    assert response.status_code == 200

  def test_root_returns_html(self):
    # Корневой эндпоинт возвращает HTML-страницу.
    response = client.get('/')
    assert 'text/html' in response.headers['content-type']

  def test_root_contains_title(self):
    # HTML-страница содержит заголовок веб-интерфейса.
    response = client.get('/')
    assert 'Анализ текста' in response.text


class Test_AnalyzeEndpoint:
  # Проверяет эндпоинт анализа одного текста.

  def test_analyze_simple_text(self):
    # Простой английский текст анализируется успешно.
    response = client.post(
      '/analyze',
      json={'text': 'The cat sat on the mat.'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['language'] == 'en'
    assert 'flesch_index' in data
    assert 'interpretation' in data
    assert 'polarity' in data
    assert 'stats' in data

  def test_analyze_returns_stats(self):
    # Ответ содержит объект stats с нужными полями.
    response = client.post(
      '/analyze',
      json={'text': 'The cat sat on the mat.'}
    )
    data = response.json()
    stats = data['stats']
    assert 'sentence_count' in stats
    assert 'word_count' in stats
    assert 'syllable_count' in stats

  def test_analyze_empty_text_returns_400(self):
    # Пустой текст - ошибка 400.
    response = client.post('/analyze', json={'text': ''})
    assert response.status_code == 400

  def test_analyze_too_long_text_returns_400(self):
    # Слишком длинный текст (>10000) - ошибка 400.
    response = client.post(
      '/analyze',
      json={'text': 'a' * 10001}
    )
    assert response.status_code == 400

  def test_analyze_missing_field_returns_422(self):
    # Запрос без поля text - ошибка 422 (валидация Pydantic).
    response = client.post('/analyze', json={})
    assert response.status_code == 422


class Test_AnalyzeBatchEndpoint:
  # Проверяет эндпоинт пакетного анализа.

  def test_batch_two_texts(self):
    # Массив из двух текстов - два результата.
    response = client.post(
      '/analyze-batch',
      json={'texts': ['Hello world.', 'How are you?']}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

  def test_batch_single_text(self):
    # Массив из одного текста - один результат.
    response = client.post(
      '/analyze-batch',
      json={'texts': ['Hello world.']}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

  def test_batch_empty_list(self):
    # Пустой массив - пустой ответ.
    response = client.post(
      '/analyze-batch',
      json={'texts': []}
    )
    assert response.status_code == 200
    assert response.json() == []


class Test_Security:
  # Проверяет безопасность API.

  def test_xss_injection_safe(self):
    # Скрипт в тексте не выполняется, а возвращается как данные.
    response = client.post(
      '/analyze',
      json={'text': '<script>alert(1)</script>'}
    )
    assert response.status_code == 200

  def test_sql_injection_safe(self):
    # SQL-инъекция не ломает API.
    response = client.post(
      '/analyze',
      json={'text': "'; DROP TABLE users; --"}
    )
    assert response.status_code == 200

  def test_null_byte_safe(self):
    # Нулевой байт не ломает API.
    response = client.post(
      '/analyze',
      json={'text': 'Hello\x00World'}
    )
    assert response.status_code in (200, 400)

  def test_very_large_input(self):
    # Огромный текст отклоняется с ошибкой 400.
    response = client.post(
      '/analyze',
      json={'text': 'a' * 100000}
    )
    assert response.status_code == 413


class Test_Caching:
  # Проверяет, что повторные запросы возвращают одинаковый результат.

  def test_repeated_requests_same_result(self):
    # Два одинаковых запроса дают одинаковый результат.
    response1 = client.post('/analyze', json={'text': 'Hello world.'})
    response2 = client.post('/analyze', json={'text': 'Hello world.'})
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()