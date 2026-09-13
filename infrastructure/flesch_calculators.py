def fleschIndex(stats: dict, lang: str) -> float:
  """
  Вычисляет индекс Флеша.

  Коэффициенты зависят от языка.
  """
  words = stats['words']
  sentences = stats['sentences']
  syllables = stats['syllables']
  if words == 0 or sentences == 0:
    return 0.0
  coefficients = {
    'en': (206.835, 1.015, 84.6),
    'ru': (206.835, 1.3, 60.1),
    'de': (206.835, 0.942, 82.3),
    'fr': (207.0, 1.015, 73.6)
  }
  coefA, coefB, coefC = coefficients.get(lang, coefficients['en'])
  score = coefA - coefB * (words / sentences) - coefC * (syllables / words)
  return score


def interpretFlesch(score: float) -> str:
  """
  Интерпретирует индекс Флеша согласно таблице из задания.
  """
  if score > 80:
    return 'Очень легко (для младших школьников)'
  elif score > 50:
    return 'Просто (для школьников)'
  elif score > 25:
    return 'Немного трудно (для студентов)'
  else:
    return 'Трудно (для выпускников вузов)'


def fleschKincaid(stats: dict, lang: str) -> float:
  """
  Вычисляет индекс Флеша-Кинкейда.

  Формула использует среднюю длину предложения
  и среднее количество слогов на слово.
  """
  words = stats['words']
  sentences = stats['sentences']
  syllables = stats['syllables']
  if words == 0 or sentences == 0:
    return 0.0
  score = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
  return score
