from dataclasses import dataclass
from enum import Enum, auto

class Language(Enum):
    EN = auto()
    RU = auto()
    DE = auto()
    FR = auto()

class Polarity(Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

@dataclass(frozen=True)
class TextStats:
    sentence_count: int
    word_count: int
    syllable_count: int
    avg_sentence_length: float
    avg_word_syllables: float

@dataclass(frozen=True)
class AnalysisResult:
    language: Language
    flesch_index: float
    flesch_kincaid: float
    interpretation: str
    polarity: Polarity
    subjectivity: float   # 0..1
    lexical_diversity: float
    rare_word_density: float
    stats: TextStats
