from deep_translator import GoogleTranslator
from app import logger
from app.database import SessionData


def fetch_langcode():
    """:returns list: E.g. [en, bn, ir, fr ...]"""
    glangCodesList = SessionData.get("glangCodesList")
    if glangCodesList:
        return glangCodesList
    
    langList = GoogleTranslator().get_supported_languages(as_dict=True)
    glangCodesList = list(langList.values())
    
    SessionData.insert(data={"glangCodesList": glangCodesList})
    return glangCodesList


def Translate(text: str, lang_code: str = "en"):
    is_language_supported = GoogleTranslator().is_language_supported(lang_code)
    if not is_language_supported:
        logger.error(f"Invalid language code! Given code: {lang_code}")
        return False
    
    try:
        return GoogleTranslator(target=lang_code).translate(text=text)
    except Exception as e:
        logger.error(e)
