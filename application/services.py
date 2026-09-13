from infrastructure.syllable_counters import countSyllablesRu, countSyllablesEn, countSyllablesDe, countSyllablesFr
from infrastructure.flesch_calculators import fleschIndex


def getSyllableCounter(lang):
  """Возвращает функцию подсчёта слогов для указанного языка."""
  counters = {
    'ru': countSyllablesRu,
    'en': countSyllablesEn,
    'de': countSyllablesDe,
    'fr': countSyllablesFr
  }
  return counters.get(lang, countSyllablesEn)


def getFleschCalculator(lang):
  """Возвращает функцию расчёта индекса Флеша для языка."""
  return fleschIndex
