from bot import logger
from base64 import b64decode, b64encode

class BASE64:
    async def decode(base64):
        try:
            decoded_text = b64decode(base64).decode("utf-8")
            if decoded_text:
                return decoded_text
        except Exception as e:
            logger.error(e)


    async def encode(text): 
        try:
            encoded_text = b64encode(text.encode("utf-8")).decode("utf-8")
            if encoded_text:
                return encoded_text
        except Exception as e:
            logger.error(e)
