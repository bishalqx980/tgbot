import aiohttp
from uuid import uuid4
from io import BytesIO
from app import logger


class GenerativeAI:
    def __init__(self):
        self.text_gen_model = "http://ai-llm.server0x01.workers.dev/"
        self.image_gen_model = "https://ai-imagine.server0x01.workers.dev/"


    async def ask(self, prompt: str, only_response: bool = True):
        """
        :param only_response: returns only response text if `True` otherwise a json response
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.text_gen_model, params={"prompt": prompt}) as response:
                    result = await response.json()
                    if only_response:
                        return result[0]["response"]["response"]
                    else:
                        return result
        except Exception as e:
            logger.error(e)
    

    async def imagine(self, prompt: str):
        """
        :returns: image buffer | `None`
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.image_gen_model, params={"prompt": prompt}) as response:
                    result = await response.read()

                    image_buffer = BytesIO(result)
                    image_buffer.name = f"{uuid4().hex}.png"

                    return image_buffer
        except Exception as e:
            logger.error(e)
