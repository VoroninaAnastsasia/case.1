from dev import getTextStats


class Test_GetTextStats:
  # Проверяет общую статистику текста.

  def test_simple_english(self):
    # Простое английское предложение.
    stats = getTextStats('The cat sat on the mat.')
    assert stats['sentences'] == 1
    assert stats['words'] == 6
    assert stats['syllables'] > 0
    assert stats['language'] == 'en'

  def test_two_sentences(self):
    # Два предложения — счётчик предложений должен быть 2.
    stats = getTextStats('Hello world. How are you?')
    assert stats['sentences'] == 2
    assert stats['words'] == 5

  def test_avg_sentence_length(self):
    # Проверка средней длины предложения.
    # 6 слов / 1 предложение = 6.0.
    stats = getTextStats('The cat sat on the mat.')
    assert stats['avg_sentence_length'] == 6.0

  def test_avg_word_length(self):
    # Проверка средней длины слова.
    # Слова: The(3) cat(3) sat(3) on(2) the(3) mat(3) = 17 / 6 ≈ 2.83.
    stats = getTextStats('The cat sat on the mat.')
    assert 2.8 < stats['avg_word_length'] < 2.9

  def test_empty_text(self):
    # Пустой текст — граничный случай.
    stats = getTextStats('')
    assert stats['sentences'] == 0
    assert stats['words'] == 0
    assert stats['syllables'] == 0

  def test_russian_text(self):
    # Русский текст.
    stats = getTextStats('Привет мир. Как дела?')
    assert stats['sentences'] == 2
    assert stats['words'] == 4

  def test_stats_keys_exist(self):
    # Проверка, что словарь содержит все нужные ключи.
    stats = getTextStats('Hello world.')
    expected_keys = ['sentences', 'words', 'syllables', 'avg_sentence_length', 'avg_word_length', 'language']
    for key in expected_keys:
      assert key in stats