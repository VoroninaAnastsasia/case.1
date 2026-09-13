from locust import HttpUser, task, between


class TextAnalyzer_User(HttpUser):
  # Симулирует пользователя, который дёргает API анализа.
  wait_time = between(1, 3)

  @task(3)
  def analyzeSingleText(self):
    # Отправляет один текст на анализ. Вес 3 — делается чаще.
    self.client.post(
      '/analyze',
      json={'text': 'The quick brown fox jumps over the lazy dog.'}
    )

  @task(1)
  def analyzeBatchTexts(self):
    # Отправляет массив текстов на пакетный анализ. Вес 1 — реже.
    self.client.post(
      '/analyze-batch',
      json={'texts': [
        'Hello world. How are you today?',
        'This is a simple test sentence.',
        'Another text for batch analysis.'
      ]}
    )

  @task(1)
  def checkHealth(self):
    # Проверяет, что сервис отвечает.
    self.client.get('/')