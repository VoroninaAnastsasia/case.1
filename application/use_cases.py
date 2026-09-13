import re

from domain.types import Language, Polarity, TextStats, AnalysisResult
from infrastructure.syllable_counters import (
  countSyllablesRu,
  countSyllablesEn,
  countSyllablesDe,
  countSyllablesFr
)
from infrastructure.flesch_calculators import (
  fleschIndex,
  interpretFlesch,
  fleschKincaid
)
from infrastructure.sentiment import analyzeSentiment
from infrastructure.language_detector import detectLanguage


# Сопоставление строки языка с Enum-значением.
LANGUAGE_MAP = {
  'en': Language.EN,
  'ru': Language.RU,
  'de': Language.DE,
  'fr': Language.FR
}


# Сопоставление строки тональности с Enum-значением.
POLARITY_MAP = {
  'Позитивная': Polarity.POSITIVE,
  'Негативная': Polarity.NEGATIVE,
  'Нейтральная': Polarity.NEUTRAL
}


def splitSentences(text):
  # Разбивает текст на предложения по знакам . ! ?
  sentences = re.split(r'[.!?]+', text)
  return [s.strip() for s in sentences if s.strip()]


def splitWords(text):
  # Извлекает слова из текста.
  return re.findall(r'\b[\wёЁа-яА-Яa-zA-Z]+\b', text, re.UNICODE)


def getSyllableCounter(lang):
  # Возвращает функцию подсчёта слогов для указанного языка.
  counters = {
    'ru': countSyllablesRu,
    'en': countSyllablesEn,
    'de': countSyllablesDe,
    'fr': countSyllablesFr
  }
  return counters.get(lang, countSyllablesEn)


def computeStats(text, syllableCounter):
  # Вычисляет статистику текста: предложения, слова, слоги, средние длины.
  sentences = splitSentences(text)
  words = splitWords(text)

  wordCount = len(words)
  sentenceCount = len(sentences)
  totalSyllables = sum(syllableCounter(w) for w in words)

  avgSentenceLength = wordCount / sentenceCount if sentenceCount else 0.0

  if wordCount:
    avgWordSyllables = totalSyllables / wordCount
  else:
    avgWordSyllables = 0.0

  return TextStats(
    sentence_count=sentenceCount,
    word_count=wordCount,
    syllable_count=totalSyllables,
    avg_sentence_length=avgSentenceLength,
    avg_word_syllables=avgWordSyllables
  )


def computeLexicalDiversity(text):
  # Вычисляет лексическое разнообразие (уникальные / все слова).
  words = splitWords(text)
  if not words:
    return 0.0
  uniqueWords = set(w.lower() for w in words)
  return len(uniqueWords) / len(words)


def computeRareWordDensity(text, freqDict):
  # Вычисляет плотность редких слов (нет в частотном словаре).
  words = splitWords(text)
  if not words:
    return 0.0
  if not freqDict:
    return 0.0
  rareCount = sum(1 for w in words if w.lower() not in freqDict)
  return rareCount / len(words)


def analyzeText(text, freqDict=None):
  # Полный анализ текста: язык, статистика, Флеш, тональность, метрики.
  if not text or not text.strip():
    raise ValueError("Текст пустой.")
  if len(text) > 10000:
    raise ValueError("Текст превышает допустимый размер (10000 символов).")

  if freqDict is None:
    freqDict = {}

  lang = detectLanguage(text)
  counter = getSyllableCounter(lang)
  stats = computeStats(text, counter)

  flesch = fleschIndex(
    {'words': stats.word_count, 'sentences': stats.sentence_count, 'syllables': stats.syllable_count},
    lang
  )
  interpretation = interpretFlesch(flesch)

  kincaid = fleschKincaid(
    {'words': stats.word_count, 'sentences': stats.sentence_count, 'syllables': stats.syllable_count},
    lang
  )

  sentimentStr, subjectivity, sentimentNote = analyzeSentiment(text, lang)
  polarity = POLARITY_MAP.get(sentimentStr, Polarity.NEUTRAL)

  diversity = computeLexicalDiversity(text)
  rareDensity = computeRareWordDensity(text, freqDict)

  result = AnalysisResult(
    language=LANGUAGE_MAP.get(lang, Language.EN),
    flesch_index=flesch,
    flesch_kincaid=kincaid,
    interpretation=interpretation,
    polarity=polarity,
    subjectivity=subjectivity / 100.0,
    lexical_diversity=diversity,
    rare_word_density=rareDensity,
    stats=stats
  )

  return result


def analyzeBatch(texts, freqDict=None):
  # Анализирует массив текстов.
  return [analyzeText(t, freqDict) for t in texts]
