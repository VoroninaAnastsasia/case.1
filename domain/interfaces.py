from typing import Protocol
from .types import Language, Polarity

class SyllableCounter(Protocol):
    def __call__(self, word: str) -> int:
        ...

class SentimentAnalyzer(Protocol):
    def __call__(self, text: str) -> tuple[Polarity, float]:
        ...

class LanguageDetector(Protocol):
    def __call__(self, text: str) -> Language:
        ...
