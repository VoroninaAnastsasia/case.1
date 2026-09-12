from dev import validateText, splitSentences, splitWords, lexicalDiversity


class Test_ValidateText:
  # Проверяет валидацию текста.

  def test_valid_text(self):
    # Обычный текст проходит проверку.
    assert validateText('Это обычный текст.') is True

  def test_empty_string(self):
    # Пустая строка не проходит.
    assert validateText('') is False

  def test_only_spaces(self):
    # Строка из пробелов не проходит.
    assert validateText('     ') is False

  def test_only_newlines(self):
    # Строка из переносов строк не проходит.
    assert validateText('\n\n\n') is False

  def test_none(self):
    # None не проходит.
    assert validateText(None) is False

  def test_too_long(self):
    # Текст длиной 10001 символ не проходит.
    long_text = 'a' * 10001
    assert validateText(long_text) is False

  def test_max_length(self):
    # Текст ровно 10000 символов проходит.
    max_text = 'a' * 10000
    assert validateText(max_text) is True


class Test_SplitSentences:
  # Проверяет разбивку текста на предложения.

  def test_simple(self):
    # Два предложения с точками.
    result = splitSentences('Привет. Как дела?')
    assert len(result) == 2
    assert result[0] == 'Привет'
    assert result[1] == 'Как дела'

  def test_exclamation(self):
    # Восклицательные знаки.
    result = splitSentences('Ура! Победа!')
    assert len(result) == 2

  def test_question(self):
    # Вопросительные знаки.
    result = splitSentences('Что? Где? Когда?')
    assert len(result) == 3

  def test_empty(self):
    # Пустой текст -> пустой список.
    assert splitSentences('') == []

  def test_only_punctuation(self):
    # Только знаки препинания -> пустой список.
    assert splitSentences('...!!!???') == []

  def test_whitespace_trim(self):
    # Пробелы вокруг предложений должны удаляться.
    result = splitSentences('  Привет.   Пока.  ')
    assert result == ['Привет', 'Пока']


class Test_SplitWords:
  # Проверяет извлечение слов из текста.

  def test_simple(self):
    # Простое предложение.
    result = splitWords('Hello world')
    assert result == ['Hello', 'world']

  def test_with_punctuation(self):
    # Знаки препинания не попадают в слова.
    result = splitWords('Hello, world!')
    assert result == ['Hello', 'world']

  def test_russian_text(self):
    # Русские слова распознаются.
    result = splitWords('Привет, мир!')
    assert result == ['Привет', 'мир']

  def test_empty(self):
    # Пустой текст -> пустой список.
    assert splitWords('') == []

  def test_numbers(self):
    # Числа тоже считаются словами (по регулярке \w+).
    result = splitWords('test 123 end')
    assert result == ['test', '123', 'end']


class Test_LexicalDiversity:
  # Проверяет лексическое разнообразие.

  def test_empty(self):
    # Пустой текст -> 0.0.
    assert lexicalDiversity('') == 0.0

  def test_all_unique(self):
    # Все слова уникальны -> коэффициент 1.0.
    result = lexicalDiversity('один два три четыре')
    assert result == 1.0

  def test_all_same(self):
    # Все слова одинаковые -> коэффициент 0.25.
    result = lexicalDiversity('да да да да')
    assert result == 0.25

  def test_mixed_case(self):
    # 'Hello' и 'hello' считаются одним словом (регистр не важен).
    result = lexicalDiversity('Hello hello')
    assert result == 0.5