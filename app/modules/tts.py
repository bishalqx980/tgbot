from uuid import uuid4
from gtts import gTTS
from io import BytesIO
from app import logger


def TextToSpeech(text: str, lang_code: str = "en"):
    """
    Convert text to speech and returns BytesIO\n
    :param text: Text to convert
    :param lang_code: Language code (default: "en")
    :returns: audio file bytes
    """
    try:
        buffer = BytesIO()

        tts = gTTS(text, lang=lang_code)
        tts.write_to_fp(buffer)

        buffer.seek(0)
        buffer.name = f"voice-{uuid4().hex}.mp3"

        return buffer
    except Exception as e:
        logger.error(e)
