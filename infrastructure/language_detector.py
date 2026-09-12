from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def detectLanguage(text): 
    """
    Определяет язык текста с помощью langdetect.
    Возвращает:
    ru - русский
    en - английский
    de - немецкий
    fr - французский
    unknown - если язык определить не удалось.
    """

    try:
      language = detect(text)
      return language
    
    except LangDetectException:
      return "unknown"
