from textblob import TextBlob
from deep_translator import GoogleTranslator


def analyzeSentiment(text: str, lang: str) -> tuple[str, float, str]:
  """
  Определяет тональность и субъективность текста.

  Для английского текста TextBlob используется напрямую.
  Для русского, немецкого и французского текста сначала выполняется
  перевод на английский язык, после чего переведённый текст
  анализируется через TextBlob.

  Возвращает:
  - тональность;
  - субъективность в процентах.
  """
  note = ''
  # Если текст не на английском, переводим его на английский.
  if lang != 'en':
    if lang not in {'ru', 'de', 'fr'}:
      return ('Нейтральная', 0.0, 'Язык не поддерживается для перевода')
    try:
      translatedText = GoogleTranslator(source=lang, target='en').translate(text)
      note = 'Текст был переведён на английский перед анализом TextBlob.'
    except Exception as error:
      return ('Нейтральная', 0.0, 'Не удалось выполнить перевод: ' + str(error))
  else:
    translatedText = text
  # Анализируем текст через TextBlob.
  blob = TextBlob(translatedText)
  polarity = blob.sentiment.polarity
  subjectivity = blob.sentiment.subjectivity * 100
  # Определяем категорию тональности.
  if polarity > 0.1:
    sentiment = 'Позитивная'
  elif polarity < -0.1:
    sentiment = 'Негативная'
  else:
    sentiment = 'Нейтральная'
  return (sentiment, subjectivity, note)
