from gtts import gTTS
from io import BytesIO
from .. import logger

def text_to_speech(text, lang_code="en"):
    """
    Convert text to speech and return audio bytes\n
    :param text: Text to convert
    :param lang_code: Language code (default: "en")
    :returns: audio file bytes
    """
    try:
        audio_buffer = BytesIO()

        tts = gTTS(text, lang=lang_code)
        tts.write_to_fp(audio_buffer)

        audio_buffer.seek(0)
        return audio_buffer.read()
    except Exception as e:
        logger.error(e)
