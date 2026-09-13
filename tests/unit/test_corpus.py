import pytest

from tests.fixtures.corpus import CORPUS
from dev import (
  detectLanguage,
  splitSentences,
  splitWords,
  getTextStats
)


class Test_CorpusLanguage:
  # Проверяет определение языка на текстах из корпуса.

  @pytest.mark.parametrize(
    'caseName',
    ['simple_english', 'two_sentences_english', 'long_english']
  )
  def test_english_cases(self, caseName):
    case = CORPUS[caseName]
    assert detectLanguage(case['text']) == 'en'

  def test_russian_case(self):
    case = CORPUS['simple_russian']
    assert detectLanguage(case['text']) == 'ru'

  def test_german_case(self):
    case = CORPUS['simple_german']
    assert detectLanguage(case['text']) == 'de'

  def test_french_case(self):
    case = CORPUS['simple_french']
    assert detectLanguage(case['text']) == 'fr'


class Test_CorpusSentences:
  # Проверяет разбивку текста на предложения.

  @pytest.mark.parametrize('caseName', list(CORPUS.keys()))
  def test_sentences_count(self, caseName):
    case = CORPUS[caseName]
    if 'sentences' not in case['expected']:
      pytest.skip('Нет эталонного значения предложений.')
    result = splitSentences(case['text'])
    assert len(result) == case['expected']['sentences']


class Test_CorpusWords:
  # Проверяет извлечение слов.

  @pytest.mark.parametrize('caseName', list(CORPUS.keys()))
  def test_words_count(self, caseName):
    case = CORPUS[caseName]
    if 'words' not in case['expected']:
      pytest.skip('Нет эталонного значения слов.')
    result = splitWords(case['text'])
    assert len(result) == case['expected']['words']


class Test_CorpusStats:
  # Проверяет общую статистику текста.

  def test_simple_english_stats(self):
    case = CORPUS['simple_english']
    stats = getTextStats(case['text'])
    assert stats['sentences'] == case['expected']['sentences']
    assert stats['words'] == case['expected']['words']
    assert stats['language'] == case['expected']['language']