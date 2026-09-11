from typing import Union
from io import BytesIO
from app import logger
from base64 import b64decode, b64encode


class BASE64:
    @staticmethod
    def decode(base64):
        try:
            return b64decode(base64).decode("UTF-8")
        except Exception as e:
            logger.error(e)


    @staticmethod
    def encode(buffer: Union[str, bytes, BytesIO]):
        """
        Encode text, bytes, or BytesIO into Base64 string.

        :param buffer: str, bytes, or BytesIO object
        """
        try:
            if isinstance(buffer, BytesIO):
                buffer = buffer.getvalue()
            
            elif isinstance(buffer, str):
                buffer = buffer.encode("UTF-8")
            
            return b64encode(buffer).decode("UTF-8")
        except Exception as e:
            logger.error(e)
