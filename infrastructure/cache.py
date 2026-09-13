import hashlib
import json
from dataclasses import asdict

import redis

from domain.types import AnalysisResult


def textHash(text):
  # Возвращает SHA-256 хеш текста для использования в качестве ключа кэша.
  return hashlib.sha256(text.encode('utf-8')).hexdigest()


def getCachedResult(redisClient, text):
  # Пытается получить результат анализа из кэша.
  # Возвращает dict или None, если в кэше ничего нет.
  key = textHash(text)
  data = redisClient.get(key)
  if data is None:
    return None
  return json.loads(data)


def setCachedResult(redisClient, text, result, ttlSeconds=3600):
  # Сохраняет результат анализа в кэш на ttlSeconds секунд.
  # result должен быть экземпляром AnalysisResult или dict.
  key = textHash(text)

  if isinstance(result, AnalysisResult):
    payload = asdict(result)
  else:
    payload = result

  # Преобразуем Enum-значения в строки для корректной сериализации в JSON.
  if 'language' in payload and hasattr(payload['language'], 'name'):
    payload['language'] = payload['language'].name
  if 'polarity' in payload and hasattr(payload['polarity'], 'name'):
    payload['polarity'] = payload['polarity'].name

  redisClient.setex(key, ttlSeconds, json.dumps(payload))
