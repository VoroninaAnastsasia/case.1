from infrastructure.syllable_counters import (
  countSyllablesRu,
  countSyllablesEn,
  countSyllablesDe,
  countSyllablesFr
)

from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentiment


def getServices():
  return {
    "language_detector": detectLanguage,
    "syllable_counters": {
      "ru": countSyllablesRu,
      "en": countSyllablesEn,
      "de": countSyllablesDe,
      "fr": countSyllablesFr
    },
    "sentiment_analyzer": analyzeSentiment
  }
