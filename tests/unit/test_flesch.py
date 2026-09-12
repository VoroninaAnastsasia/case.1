from dev import interpretFlesch, fleschIndex, fleschKincaid


class Test_InterpretFlesch:
  # Проверяет границы интерпретации индекса Флеша.

  def test_very_easy(self):
    # > 80 — очень легко.
    assert 'Очень легко' in interpretFlesch(90)
    assert 'Очень легко' in interpretFlesch(100)

  def test_easy(self):
    # 50 < score <= 80 — просто.
    assert 'Просто' in interpretFlesch(60)
    assert 'Просто' in interpretFlesch(80)

  def test_little_hard(self):
    # 25 < score <= 50 — немного трудно.
    assert 'Немного трудно' in interpretFlesch(30)
    assert 'Немного трудно' in interpretFlesch(50)

  def test_hard(self):
    # score <= 25 — трудно.
    assert 'Трудно' in interpretFlesch(0)
    assert 'Трудно' in interpretFlesch(25)


class Test_FleschIndex:
  # Проверяет вычисление индекса Флеша.

  def test_empty_stats(self):
    # Пустая статистика -> 0.0.
    stats = {'words': 0, 'sentences': 0, 'syllables': 0}
    assert fleschIndex(stats, 'en') == 0.0

  def test_english_simple(self):
    # Простой английский текст -> высокий балл.
    stats = {'words': 20, 'sentences': 2, 'syllables': 24}
    score = fleschIndex(stats, 'en')
    assert score > 50

  def test_russian_text(self):
    # Русский текст должен обрабатываться по своим коэффициентам.
    stats = {'words': 20, 'sentences': 2, 'syllables': 30}
    score = fleschIndex(stats, 'ru')
    assert score is not None


class Test_FleschKincaid:
  # Проверяет индекс Флеша-Кинкейда.

  def test_empty_stats(self):
    stats = {'words': 0, 'sentences': 0, 'syllables': 0}
    assert fleschKincaid(stats, 'en') == 0.0

  def test_basic(self):
    stats = {'words': 20, 'sentences': 2, 'syllables': 24}
    score = fleschKincaid(stats, 'en')
    assert score > 0