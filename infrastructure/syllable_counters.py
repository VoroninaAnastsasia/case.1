def countSyllablesRu(text: str) -> int:
  """
  Подсчёт слогов в русском тексте.
  """
  vowels = set('аеёиоуыэюяАЕЁИОУЫЭЮЯ')
  return max(1, sum(1 for char in text if char in vowels))


def countSyllablesEn(text: str) -> int:
  """
  Подсчёт слогов в английском тексте.

  Используется алгоритм с несколькими словами-исключениями.
  """
  text = text.lower()
  exceptions = {
    'beautiful': 3, 'people': 2, 'business': 2, 'different': 3,
    'family': 3, 'every': 2, 'favorite': 3, 'chocolate': 3,
    'comfortable': 4, 'interesting': 3, 'restaurant': 3,
    'temperature': 4, 'education': 4, 'environment': 4, 'information': 4
  }
  if text in exceptions:
    return exceptions[text]
  vowels = set('aeiouy')
  count = 0
  prevIsVowel = False
  for char in text:
    if char in vowels:
      if not prevIsVowel:
        count += 1
      prevIsVowel = True
    else:
      prevIsVowel = False
  # Немая e в конце слова.
  if text.endswith('e') and count > 1:
    count -= 1
  # Упрощённая обработка окончания -le.
  if text.endswith('le') and len(text) > 2:
    count += 1
  return max(1, count)


def countSyllablesDe(text: str) -> int:
  """
  Подсчёт слогов в немецком тексте.

  Используется упрощённый алгоритм с исключениями.
  """
  text = text.lower()
  exceptions = {
    'hallo': 2, 'deutsch': 1, 'liebe': 2, 'bitte': 2, 'danke': 2,
    'machen': 2, 'lehrer': 2, 'schule': 2, 'apfel': 2, 'freund': 1,
    'familie': 3, 'computer': 3, 'telefon': 3, 'universität': 5,
    'freundschaft': 2
  }
  if text in exceptions:
    return exceptions[text]
  vowels = set('aeiouyäöü')
  count = 0
  prevIsVowel = False
  for char in text:
    if char in vowels:
      if not prevIsVowel:
        count += 1
      prevIsVowel = True
    else:
      prevIsVowel = False
  return max(1, count)


def countSyllablesFr(text: str) -> int:
  """
  Подсчёт слогов во французском тексте.

  Используется упрощённый алгоритм с исключениями.
  """
  text = text.lower()
  exceptions = {
    'bonjour': 2, 'ordinateur': 4, 'français': 2, 'france': 1,
    'femme': 1, 'monsieur': 2, 'beaucoup': 2, 'oiseau': 2, 'eau': 1,
    'fille': 1, 'garçon': 2, 'maison': 2, 'voiture': 2, 'école': 2,
    'famille': 2, 'question': 2, 'important': 3, 'maintenant': 3,
    'aujourd\'hui': 3
  }
  if text in exceptions:
    return exceptions[text]
  vowels = set('aeiouyàâäéèêëîïôöùûüÿ')
  count = 0
  prevIsVowel = False
  for char in text:
    if char in vowels:
      if not prevIsVowel:
        count += 1
      prevIsVowel = True
    else:
      prevIsVowel = False
  return max(1, count)
