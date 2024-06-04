import g4f
from bot import logger

class G4F:
    async def chatgpt(prompt):
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response
        except Exception as e:
            logger.error(e)


    async def imagine(prompt):
        try:
            response = g4f.images.generate(
            model="stability-ai/sdxl",
            prompt=prompt
            )
            image_url = response.data[0].url
            return image_url
        except Exception as e:
            logger.error(e)
