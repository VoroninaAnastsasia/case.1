import hashlib, json, redis
from dataclasses import asdict
from domain.types import AnalysisResult


# Единственное подключение к Redis (создаётся один раз).
redisClient = redis.Redis(host='localhost', port=6379, decode_responses=True)


def textHash(text):
  # Возвращает SHA-256 хеш текста для использования в качестве ключа кэша.
  return hashlib.sha256(text.encode('utf-8')).hexdigest()


def getCachedResult(text):
  # Пытается получить результат анализа из кэша.
  # Возвращает dict или None.
  try:
    key = textHash(text)
    data = redisClient.get(key)
    if data is None:
      return None
    return json.loads(data)
  except redis.RedisError:
    # Если Redis недоступен, работаем без кэша.
    return None


def setCachedResult(text, result, ttlSeconds=3600):
  # Сохраняет результат анализа в кэш на ttlSeconds секунд.
  try:
    key = textHash(text)
    if isinstance(result, AnalysisResult):
      payload = asdict(result)
    else:
      payload = result
    # Преобразуем Enum-значения в строки для JSON.
    if 'language' in payload and hasattr(payload['language'], 'name'):
      payload['language'] = payload['language'].name
    if 'polarity' in payload and hasattr(payload['polarity'], 'name'):
      payload['polarity'] = payload['polarity'].name
    redisClient.setex(key, ttlSeconds, json.dumps(payload))
  except redis.RedisError:
    # Если Redis недоступен, просто не кэшируем.
    pass
