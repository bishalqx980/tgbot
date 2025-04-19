import aiohttp
from io import BytesIO
from bot import logger

class LLM:
    def __init__(self):
        self.text_gen_model = "http://ai-llm.server0x01.workers.dev/"
        self.image_gen_model = "https://ai-imagine.server0x01.workers.dev/"


    async def text_gen(self, prompt, only_response=True):
        """
        :param only_response: returns only response text if `True`
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
    

    async def imagine(self, prompt):
        """
        :returns: image byte | `None`
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.image_gen_model, params={"prompt": prompt}) as response:
                    result = await response.read()

                    image_bytes = BytesIO(result)
                    image_bytes.name = "imagine.png"

                    return image_bytes
        except Exception as e:
            logger.error(e)
