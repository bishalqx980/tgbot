from gtts import gTTS
from bot import logger

def text_to_speech(text, lang_code="en", voice_path="temp/tts.mp3"):
    try:
        tts = gTTS(text, lang=lang_code)
        tts.save(voice_path)
        return voice_path
    except Exception as e:
        logger.error(e)
