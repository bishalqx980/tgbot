import requests
from telegraph.aio import Telegraph
from bot import ORIGINAL_BOT_USERNAME, logger

class TELEGRAPH:
    def __init__(self):
        self.telegraph = None
        self.domain = "telegra.ph"


    async def initialize(self):
        domain_names = ["telegra.ph", "graph.org"]
        for domain in domain_names:
            try:
                response = requests.get(f"https://{domain}", timeout=3)
                if response.ok:
                    logger.info(f"Telegraph initialized! Domain: https://{domain}")
                    break
            except Exception as e:
                logger.error(e)
        
        self.telegraph = Telegraph(domain=domain)
        await self.telegraph.create_account(f"@{ORIGINAL_BOT_USERNAME}")


    async def paste(self, text, username="anonymous"):
        """
        :param text: supports HTML format
        """
        try:
            path = await self.telegraph.create_page(
                f"{username} - @{ORIGINAL_BOT_USERNAME}",
                html_content=text.replace("\n", "<br>"), # replacing \n with <br>
                author_name=f"{username} using @{ORIGINAL_BOT_USERNAME}",
                author_url=f"https://t.me/{ORIGINAL_BOT_USERNAME}"
            )
            
            return path.get("url")
        except Exception as e:
            logger.error(e)


    async def upload_img(self, image_path):
        try:
            path = await self.telegraph.upload_file(image_path)[0]
            link = f"https://{self.domain}{path.get('src')}"
            return link
        except Exception as e:
            logger.error(e)
