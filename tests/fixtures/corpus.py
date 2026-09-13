"""Тестовый корпус с эталонными значениями."""

CORPUS = {
  'simple_english': {
    'text': 'The cat sat on the mat.',
    'expected': {
      'language': 'en',
      'sentences': 1,
      'words': 6,
      'min_syllables': 5,
      'max_syllables': 7
    }
  },

  'two_sentences_english': {
    'text': 'Hello world. How are you?',
    'expected': {
      'language': 'en',
      'sentences': 2,
      'words': 5
    }
  },

  'positive_english': {
    'text': 'I love this beautiful sunny day and I am very happy.',
    'expected': {
      'language': 'en',
      'sentences': 1,
      'polarity': 'Позитивная'
    }
  },

  'negative_english': {
    'text': 'I hate this terrible situation and I am very sad.',
    'expected': {
      'language': 'en',
      'sentences': 1,
      'polarity': 'Негативная'
    }
  },

    'simple_russian': {
    'text': 'Это простой русский текст для проверки определения языка. Он содержит несколько предложений и достаточно слов, чтобы langdetect уверенно определил русский язык.',
    'expected': {
      'language': 'ru',
      'sentences': 2
    }
  },

  'russian_positive': {
    'text': 'Я очень люблю этот прекрасный солнечный день и я счастлив.',
    'expected': {
      'language': 'ru',
      'sentences': 1
    }
  },

  'simple_german': {
    'text': (
      'Der schnelle braune Fuchs springt über den faulen Hund '
      'und läuft schnell in den Wald.'
    ),
    'expected': {
      'language': 'de',
      'sentences': 1
    }
  },

  'simple_french': {
    'text': (
      'Le rapide renard brun saute par-dessus le chien paresseux '
      'et court rapidement dans la forêt.'
    ),
    'expected': {
      'language': 'fr',
      'sentences': 1
    }
  },

  'empty_like_text': {
    'text': '...',
    'expected': {
      'sentences': 0,
      'words': 0
    }
  },

  'long_english': {
    'text': (
      'The quick brown fox jumps over the lazy dog. '
      'This is a simple test sentence for analysis. '
      'It contains multiple sentences and words.'
    ),
    'expected': {
      'language': 'en',
      'sentences': 3,
      'words': 23
    }
  }
}