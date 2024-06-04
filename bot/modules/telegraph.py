from telegraph import Telegraph
from bot import logger

telegraph = Telegraph()
telegraph.create_account("YOUR_NIGHTMARE")

class TELEGRAPH:
    async def upload_img(image_path):
        try:
            path = telegraph.upload_file(image_path)[0]
            link = f"https://telegra.ph{path.get('src')}"
            return link
        except Exception as e:
            logger.error(e)
