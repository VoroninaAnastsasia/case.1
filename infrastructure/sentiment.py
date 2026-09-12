import re
from textblob import TextBlob
from deep_translator import GoogleTranslator

def analyzeSentiment(
    text: str,
    lang: str
) -> tuple[str, float, str]:
    """
    Определяет тональность и субъективность текста.

    Для английского текста TextBlob используется напрямую.

    Для русского, немецкого и французского текста
    сначала выполняется перевод на английский язык,
    после чего переведённый текст анализируется через TextBlob.

    Возвращает:
    - тональность;
    - субъективность в процентах;
    - дополнительное сообщение.
    """

    note = ""

    # Если текст не на английском, переводим его на английский.

    if lang != "en":

        if lang not in {"ru", "de", "fr"}:

            return (
                "Нейтральная",
                0.0,
                "Язык не поддерживается для перевода"
            )

        try:
            sentences = re.split(r'(?<=[.!?])\s+', text)

            translated_sentences = []

            for sentence in sentences:
                if sentence.strip():
                    translated_sentence = GoogleTranslator(
                        source=lang,
                        target="en"
                    ).translate(sentence)
                    translated_sentences.append(translated_sentence)

            translated_text = " ".join(translated_sentences)

            note = (
                "Текст был переведён на английский "
                "перед анализом TextBlob."
            )

        except Exception as error:
            return (
                "Нейтральная",
                0.0,
                "Не удалось выполнить перевод: "
                + str(error)
            )

    # Для английского текста перевод не нужен.
    if lang == "en":
        translated_text = text

    # Анализируем текст через TextBlob.
    blob = TextBlob(
        translated_text
    )

    polarity = blob.sentiment.polarity

    subjectivity = (
        blob.sentiment.subjectivity * 100
    )

    # Определяем категорию тональности.

    if polarity > 0.1:

        sentiment = "Позитивная"

    elif polarity < -0.1:

        sentiment = "Негативная"

    else:

        sentiment = "Нейтральная"

    return (
        sentiment,
        subjectivity,
        note
    )
