from g4f.client import Client
from bot import logger

client = Client()

class G4F:
    async def chatgpt(prompt):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(e)


    async def imagine(prompt):
        try:
            response = client.images.generate(
                model="gemini",
                prompt=prompt
            )
            image_url = response.data[0].url
            return image_url
        except Exception as e:
            logger.error(e)
