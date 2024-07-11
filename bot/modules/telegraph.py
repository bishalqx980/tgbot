from telegraph import Telegraph
from bot import logger

telegraph = Telegraph()
telegraph.create_account("@MissCiri_bot")

class TELEGRAPH:
    async def paste(text, username="anonymous"):
        """
        use <br> instead of \.n
        """
        try:
            path = telegraph.create_page(f"{username} - @MissCiri_bot", html_content=text, author_name=f"{username} using @MissCiri_bot", author_url="https://t.me/MissCiri_bot")
            return path.get("url")
        except Exception as e:
            logger.error(e)


    async def upload_img(image_path):
        try:
            path = telegraph.upload_file(image_path)[0]
            link = f"https://telegra.ph{path.get('src')}"
            return link
        except Exception as e:
            logger.error(e)
