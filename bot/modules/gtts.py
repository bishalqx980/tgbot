from gtts import gTTS
from bot import logger

async def tts(text, lang_code="en"):
    try:
        tts = gTTS(text, lang=lang_code)
        voice_path = "temp/tts.mp3"
        tts.save(voice_path)
        return voice_path
    except Exception as e:
        logger.error(e)
