from infrastructure.syllable_counters import countSyllablesRu, countSyllablesEn, countSyllablesDe, countSyllablesFr


class Test_Module_Syllables_Ru:
  # Проверяет модуль подсчёта слогов для русского.

  def test_privet(self):
    # 'привет' -> 2 слога.
    assert countSyllablesRu('привет') == 2

  def test_moloko(self):
    # 'молоко' -> 3 слога.
    assert countSyllablesRu('молоко') == 3

  def test_single_vowel(self):
    # 'я' -> 1 слог.
    assert countSyllablesRu('я') == 1

  def test_no_vowels(self):
    # 'брр' -> минимум 1 слог.
    assert countSyllablesRu('брр') == 1

  def test_uppercase(self):
    # 'ПРИВЕТ' -> 2 слога.
    assert countSyllablesRu('ПРИВЕТ') == 2


class Test_Module_Syllables_En:
  # Проверяет модуль подсчёта слогов для английского.

  def test_hello(self):
    # 'hello' -> 2 слога.
    assert countSyllablesEn('hello') == 2

  def test_exception_beautiful(self):
    # Слово из исключений -> 3 слога.
    assert countSyllablesEn('beautiful') == 3

  def test_exception_people(self):
    # Слово из исключений -> 2 слога.
    assert countSyllablesEn('people') == 2

  def test_simple_word(self):
    # 'cat' -> 1 слог.
    assert countSyllablesEn('cat') == 1

  def test_silent_e(self):
    # 'make' -> немая 'e' -> 1 слог.
    assert countSyllablesEn('make') == 1

  def test_ending_le(self):
    # 'apple' -> окончание '-le' -> 2 слога.
    assert countSyllablesEn('apple') == 2


class Test_Module_Syllables_De:
  # Проверяет модуль подсчёта слогов для немецкого.

  def test_hallo(self):
    # Слово из исключений -> 2 слога.
    assert countSyllablesDe('hallo') == 2

  def test_danke(self):
    # Слово из исключений -> 2 слога.
    assert countSyllablesDe('danke') == 2

  def test_umlaut(self):
    # Слово с умляутом -> минимум 1 слог.
    assert countSyllablesDe('schön') >= 1

  def test_simple_word(self):
    # 'hund' -> 1 слог.
    assert countSyllablesDe('hund') >= 1


class Test_Module_Syllables_Fr:
  # Проверяет модуль подсчёта слогов для французского.

  def test_bonjour(self):
    # Слово из исключений -> 2 слога.
    assert countSyllablesFr('bonjour') == 2

  def test_ordinateur(self):
    # Слово из исключений -> 4 слога.
    assert countSyllablesFr('ordinateur') == 4

  def test_france(self):
    # Слово из исключений -> 1 слог.
    assert countSyllablesFr('france') == 1

  def test_simple_word(self):
    # 'chat' -> минимум 1 слог.
    assert countSyllablesFr('chat') >= 1