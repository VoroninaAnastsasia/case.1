from dev import countSyllablesRu, countSyllablesEn, countSyllablesDe, countSyllablesFr


class Test_SyllablesRu:
  # Проверяет подсчёт слогов в русских словах.

  def test_privet(self):
    # Слово 'привет' содержит 2 гласные -> 2 слога.
    assert countSyllablesRu('привет') == 2

  def test_moloko(self):
    # Слово 'молоко' содержит 3 гласные -> 3 слога.
    assert countSyllablesRu('молоко') == 3

  def test_single_vowel(self):
    # Слово 'я' содержит одну гласную -> 1 слог.
    assert countSyllablesRu('я') == 1

  def test_no_vowels(self):
    # Даже если гласных нет, функция возвращает минимум 1.
    assert countSyllablesRu('брр') == 1


class Test_SyllablesEn:
  # Проверяет подсчёт слогов в английских словах.

  def test_hello(self):
    # 'hello' -> 2 слога.
    assert countSyllablesEn('hello') == 2

  def test_exception_beautiful(self):
    # Слово из словаря исключений -> 3 слога.
    assert countSyllablesEn('beautiful') == 3

  def test_exception_people(self):
    # Слово из словаря исключений -> 2 слога.
    assert countSyllablesEn('people') == 2

  def test_simple_word(self):
    # 'cat' -> 1 слог.
    assert countSyllablesEn('cat') == 1

  def test_silent_e(self):
    # 'make' -> немая e в конце не считается -> 1 слог.
    assert countSyllablesEn('make') == 1


class Test_SyllablesDe:
  # Проверяет подсчёт слогов в немецких словах.

  def test_hallo(self):
    # Слово из словаря исключений -> 2 слога.
    assert countSyllablesDe('hallo') == 2

  def test_danke(self):
    # Слово из словаря исключений -> 2 слога.
    assert countSyllablesDe('danke') == 2

  def test_deutsch(self):
    # Слово из словаря исключений -> 1 слог.
    assert countSyllablesDe('deutsch') == 1


class Test_SyllablesFr:
  # Проверяет подсчёт слогов во французских словах.

  def test_bonjour(self):
    # Слово из словаря исключений -> 2 слога.
    assert countSyllablesFr('bonjour') == 2

  def test_ordinateur(self):
    # Слово из словаря исключений -> 4 слога.
    assert countSyllablesFr('ordinateur') == 4

  def test_france(self):
    # Слово из словаря исключений -> 1 слог.
    assert countSyllablesFr('france') == 1


class TestEnglishSyllables:
    def test_hello(self):
        assert countSyllablesEn("hello") == 2

    def test_exception_beautiful(self):
        # Слово из словаря исключений
        assert countSyllablesEn("beautiful") == 3

    def test_exception_people(self):
        assert countSyllablesEn("people") == 2

    def test_simple_word(self):
        assert countSyllablesEn("cat") == 1