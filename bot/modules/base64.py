from .. import logger
from base64 import b64decode, b64encode

class BASE64:
    def decode(base64):
        try:
            decoded_text = b64decode(base64).decode("utf-8")
            return decoded_text if decoded_text else None
        except Exception as e:
            logger.error(e)


    def encode(text): 
        try:
            encoded_text = b64encode(text.encode("utf-8")).decode("utf-8")
            return encoded_text if encoded_text else None
        except Exception as e:
            logger.error(e)
