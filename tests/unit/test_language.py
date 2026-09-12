from dev import detectLanguage, rareWordDensity, load_frequency_dictionary


class Test_DetectLanguage:
  # Проверяет определение языка текста.

  def test_english_text(self):
    # Длинный однозначный английский текст.
    text = 'The quick brown fox jumps over the lazy dog and then runs away quickly into the forest.'
    assert detectLanguage(text) == 'en'

  def test_russian_text(self):
    # Длинный однозначный русский текст.
    text = 'Быстрая коричневая лиса прыгает через ленивую собаку и быстро убегает в лес.'
    assert detectLanguage(text) == 'ru'

  def test_german_text(self):
    # Длинный однозначный немецкий текст.
    text = 'Der schnelle braune Fuchs springt über den faulen Hund und läuft schnell in den Wald.'
    assert detectLanguage(text) == 'de'

  def test_french_text(self):
    # Длинный однозначный французский текст.
    text = 'Le rapide renard brun saute par-dessus le chien paresseux et court rapidement dans la forêt.'
    assert detectLanguage(text) == 'fr'

  def test_short_text_unknown(self):
    # Слишком короткий текст — langdetect может вернуть что угодно,
    # но не должен бросать исключение.
    result = detectLanguage('a')
    assert isinstance(result, str)


class Test_RareWordDensity:
  # Проверяет плотность редких слов.

  def test_empty_text(self):
    # Пустой текст -> 0.0.
    assert rareWordDensity('', {'the': 1}) == 0.0

  def test_empty_dict(self):
    # Пустой частотный словарь -> None.
    assert rareWordDensity('hello world', {}) is None

  def test_none_dict(self):
    # None вместо словаря -> None.
    assert rareWordDensity('hello world', None) is None

  def test_all_rare(self):
    # Ни одно слово не входит в словарь -> коэффициент 1.0.
    result = rareWordDensity('apple banana cherry', {'the': 1})
    assert result == 1.0

  def test_all_common(self):
    # Все слова входят в словарь -> коэффициент 0.0.
    result = rareWordDensity('the and of', {'the': 1, 'and': 1, 'of': 1})
    assert result == 0.0

  def test_mixed(self):
    # Половина слов редкие -> коэффициент 0.5.
    result = rareWordDensity('the apple', {'the': 1})
    assert result == 0.5


class Test_LoadFrequencyDictionary:
  # Проверяет загрузку частотного словаря из файла.

  def test_nonexistent_file(self):
    # Несуществующий файл -> пустой словарь.
    result = load_frequency_dictionary('nonexistent_file_12345.txt')
    assert result == {}

  def test_frequency_file_exists(self):
    # У вас в проекте есть файл frequency.txt — проверяем, что он загружается.
    result = load_frequency_dictionary('frequency.txt')
    assert isinstance(result, dict)