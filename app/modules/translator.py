from deep_translator import GoogleTranslator
from app import logger
from app.database import SessionData


class TRANSLATOR:
    def __init__(self):
        self.engine = GoogleTranslator()

    
    def lang_codes(self) -> list:
        """:returns list: E.g. [en, bn, ir, fr ...]"""

        cached_codes = SessionData.get("deepLangCodes")
        # Return cached languages
        if cached_codes:
            return cached_codes

        try:
            lang_list = self.engine.get_supported_languages(as_dict=True)

            # Dictionary keys are the language codes
            deep_lang_codes = list(lang_list.keys())

            SessionData.insert(
                identifier="deepLangCodes",
                data=deep_lang_codes
            )

            return deep_lang_codes

        except Exception as e:
            logger.error(f"Failed to get supported languages: {e}")
            return []


    def translate(self, text: str, lang_code: str = "en") -> str:
        if not text:
            return "No text provided."

        if not self.engine.is_language_supported(lang_code):
            logger.error(
                f"Invalid language code! Given code: {lang_code}"
            )
            return f"Invalid language code! Given code: {lang_code}"

        try:
            return self.engine.translate(
                text=text,
                target=lang_code
            )

        except Exception as e:
            logger.error(f"Translation error: {e}")
            return f"Error: {e}"
