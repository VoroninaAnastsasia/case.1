from unittest.mock import patch
import fakeredis

from infrastructure.cache import getCachedResult, setCachedResult, textHash


class Test_Cache_Basic:
  # Проверяет базовые операции кэша.

  @patch('infrastructure.cache.redisClient')
  def test_set_and_get(self, mockRedis):
    # Сохраняем и читаем — данные не теряются.
    fake = fakeredis.FakeStrictRedis()
    mockRedis.get = fake.get
    mockRedis.setex = fake.setex

    setCachedResult('hello', {'language': 'en', 'flesch_index': 75.0})
    result = getCachedResult('hello')
    assert result['language'] == 'en'
    assert result['flesch_index'] == 75.0

  @patch('infrastructure.cache.redisClient')
  def test_get_missing_returns_none(self, mockRedis):
    # Если в кэше нет — возвращается None.
    fake = fakeredis.FakeStrictRedis()
    mockRedis.get = fake.get

    assert getCachedResult('nonexistent') is None

  @patch('infrastructure.cache.redisClient')
  def test_different_texts_different_keys(self, mockRedis):
    # Разные тексты — разные ключи.
    fake = fakeredis.FakeStrictRedis()
    mockRedis.get = fake.get
    mockRedis.setex = fake.setex

    setCachedResult('hello', {'result': 1})
    setCachedResult('world', {'result': 2})
    assert getCachedResult('hello')['result'] == 1
    assert getCachedResult('world')['result'] == 2

  @patch('infrastructure.cache.redisClient')
  def test_same_text_overwrites(self, mockRedis):
    # Одинаковый текст перезаписывает результат.
    fake = fakeredis.FakeStrictRedis()
    mockRedis.get = fake.get
    mockRedis.setex = fake.setex

    setCachedResult('hello', {'result': 1})
    setCachedResult('hello', {'result': 2})
    assert getCachedResult('hello')['result'] == 2

  @patch('infrastructure.cache.redisClient')
  def test_ttl_set(self, mockRedis):
    # Проверяет, что ключ создаётся с TTL.
    fake = fakeredis.FakeStrictRedis()
    mockRedis.get = fake.get
    mockRedis.setex = fake.setex

    setCachedResult('hello', {'result': 1}, ttlSeconds=3600)
    key = textHash('hello')
    ttl = fake.ttl(key)
    assert 0 < ttl <= 3600

  def test_text_hash_consistent(self):
    # Одинаковый текст даёт одинаковый хеш.
    assert textHash('hello') == textHash('hello')

  def test_text_hash_different(self):
    # Разные тексты дают разные хеши.
    assert textHash('hello') != textHash('world')