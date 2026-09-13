import re


def splitSentences(text: str) -> list[str]:
  """
  Разбивает текст на предложения.

  Используются знаки . ! ?
  """
  sentences = re.split(r'[.!?]+', text)
  return [sentence.strip() for sentence in sentences if sentence.strip()]


def splitWords(text: str) -> list[str]:
  """
  Извлекает слова из текста.
  """
  return re.findall(r'\b[\wёЁа-яА-Яa-zA-Z]+\b', text, re.UNICODE)
