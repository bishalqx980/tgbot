from deep_translator import GoogleTranslator
from bot import logger

def fetch_lang_codes():
    """:returns list: Example: [en, bn, ir, fr ...]"""
    langList = GoogleTranslator().get_supported_languages(as_dict=True)
    langCodesList = []
    for lang in langList:
        langCodesList.append(langList[lang])
    return langCodesList


def translate(text, lang_code="en"):
    is_language_supported = GoogleTranslator().is_language_supported(lang_code)
    if not is_language_supported:
        logger.error(f"Invalid language code! Given code: {lang_code}")
        return False
    
    try:
        return GoogleTranslator(target=lang_code).translate(text=text)
    except Exception as e:
        logger.error(e)
