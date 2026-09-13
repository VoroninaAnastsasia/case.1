from langdetect import detect, LangDetectException


def detectLanguage(text: str) -> str:
  # Определяет язык текста с помощью langdetect.
  # Возвращает: ru, en, de, fr или unknown.
  try:
    language = detect(text)
    return language
  except LangDetectException:
    return 'unknown'
