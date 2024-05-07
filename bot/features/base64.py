from bot import logger
from base64 import b64decode, b64encode

def decode_b64(text):
    try:
        logger.info(f"Decoding: {text}")
        decoded_text = b64decode(text).decode("utf-8")
        if decoded_text:
            logger.info(f"Decoded: {decoded_text}")
            return decoded_text
    except Exception as e:
        logger.error(f"Error (Decoding): {e}")


def encode_b64(text): 
    try:
        logger.info(f"Encoding: {text}")
        encoded_text = b64encode(text.encode("utf-8")).decode("utf-8")
        if encoded_text:
            logger.info(f"Encoded: {encoded_text}")
            return encoded_text
    except Exception as e:
        logger.error(f"Error (Encoding): {e}")
