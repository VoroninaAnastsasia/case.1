from unittest.mock import patch, MagicMock
from dev import analyzeSentiment


class Test_SentimentEnglish:
  # Проверяет анализ тональности для английского текста (без перевода).

  @patch('dev.TextBlob')
  def test_positive_english(self, mock_blob):
    # TextBlob возвращает positive polarity.
    instance = MagicMock()
    instance.sentiment.polarity = 0.8
    instance.sentiment.subjectivity = 0.6
    mock_blob.return_value = instance

    sentiment, subjectivity, note = analyzeSentiment('I love it!', 'en')
    assert sentiment == 'Позитивная'
    assert subjectivity == 60.0
    assert note == ''

  @patch('dev.TextBlob')
  def test_negative_english(self, mock_blob):
    # TextBlob возвращает negative polarity.
    instance = MagicMock()
    instance.sentiment.polarity = -0.7
    instance.sentiment.subjectivity = 0.5
    mock_blob.return_value = instance

    sentiment, subjectivity, note = analyzeSentiment('I hate it!', 'en')
    assert sentiment == 'Негативная'
    assert subjectivity == 50.0

  @patch('dev.TextBlob')
  def test_neutral_english(self, mock_blob):
    # TextBlob возвращает нулевую polarity.
    instance = MagicMock()
    instance.sentiment.polarity = 0.0
    instance.sentiment.subjectivity = 0.0
    mock_blob.return_value = instance

    sentiment, subjectivity, note = analyzeSentiment('It is a table.', 'en')
    assert sentiment == 'Нейтральная'
    assert subjectivity == 0.0


class Test_SentimentTranslation:
  # Проверяет анализ с переводом (ru, de, fr).

  @patch('dev.TextBlob')
  @patch('dev.GoogleTranslator')
  def test_russian_positive(self, mock_translator, mock_blob):
    # Мокаем перевод и TextBlob.
    mock_translator.return_value.translate.return_value = 'I love it'

    instance = MagicMock()
    instance.sentiment.polarity = 0.9
    instance.sentiment.subjectivity = 0.7
    mock_blob.return_value = instance

    sentiment, subjectivity, note = analyzeSentiment('Я люблю это', 'ru')
    assert sentiment == 'Позитивная'
    assert 'переведён' in note

  @patch('dev.TextBlob')
  @patch('dev.GoogleTranslator')
  def test_german_negative(self, mock_translator, mock_blob):
    mock_translator.return_value.translate.return_value = 'I hate it'

    instance = MagicMock()
    instance.sentiment.polarity = -0.8
    instance.sentiment.subjectivity = 0.6
    mock_blob.return_value = instance

    sentiment, subjectivity, note = analyzeSentiment('Ich hasse es', 'de')
    assert sentiment == 'Негативная'
    assert 'переведён' in note

  @patch('dev.TextBlob')
  @patch('dev.GoogleTranslator')
  def test_french_neutral(self, mock_translator, mock_blob):
    mock_translator.return_value.translate.return_value = 'It is a table'

    instance = MagicMock()
    instance.sentiment.polarity = 0.0
    instance.sentiment.subjectivity = 0.1
    mock_blob.return_value = instance

    sentiment, subjectivity, note = analyzeSentiment('C\'est une table', 'fr')
    assert sentiment == 'Нейтральная'


class Test_SentimentErrors:
  # Проверяет ошибочные случаи.

  def test_unsupported_language(self):
    # Язык 'zh' не поддерживается -> сообщение об ошибке.
    sentiment, subjectivity, note = analyzeSentiment('你好', 'zh')
    assert sentiment == 'Нейтральная'
    assert subjectivity == 0.0
    assert 'не поддерживается' in note.lower()

  @patch('dev.GoogleTranslator')
  def test_translation_error(self, mock_translator):
    # GoogleTranslator бросает исключение -> ловим и возвращаем сообщение.
    mock_translator.return_value.translate.side_effect = Exception('Network error')

    sentiment, subjectivity, note = analyzeSentiment('Привет', 'ru')
    assert sentiment == 'Нейтральная'
    assert subjectivity == 0.0
    assert 'Не удалось выполнить перевод' in note