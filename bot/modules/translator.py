from deep_translator import GoogleTranslator

async def translate(text, lang_code="en"):
    translated_text = GoogleTranslator(source='auto', target=lang_code).translate(text=text)
    return translated_text