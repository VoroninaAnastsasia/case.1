from locust import HttpUser, task, between


class TextAnalyzer_User(HttpUser):
  """Симулирует пользователя, который использует API анализа текста."""

  host = 'http://127.0.0.1:8000'
  wait_time = between(1, 3)

  @task(3)
  def analyzeSingleText(self):
    """Отправляет один текст на анализ."""
    self.client.post(
      '/analyze',
      json={'text': 'The quick brown fox jumps over the lazy dog.'},
      name='Analyze single text'
    )

  @task(1)
  def analyzeBatchTexts(self):
    """Отправляет список текстов на пакетный анализ."""
    self.client.post(
      '/analyze-batch',
      json={'texts': [
        'Hello world. How are you today?',
        'This is a simple test sentence.',
        'Another text for batch analysis.'
      ]},
      name='Analyze batch texts'
    )

  @task(1)
  def checkHealth(self):
    """Проверяет доступность сервиса."""
    self.client.get(
      '/',
      name='Health check'
    )