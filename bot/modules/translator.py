from deep_translator import GoogleTranslator
from bot import logger

def fetch_lang_codes(as_dict):
    """
    return the supported languages by the Google translator :param as_dict: if True, the languages will be returned as a dictionary mapping languages to their abbreviations :returns: list or dict :rtype:
    """
    return GoogleTranslator.get_supported_languages(as_dict=as_dict)


def translate(text, lang_code="en"):
    is_language_supported = GoogleTranslator.is_language_supported(lang_code)
    if not is_language_supported:
        logger.error(f"Invalid language code! Given code: {lang_code}")
        return False
    
    try:
        translated_text = GoogleTranslator(source='auto', target=lang_code).translate(text=text)
        return translated_text
    except Exception as e:
        logger.error(e)
