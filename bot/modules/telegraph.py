import requests
from telegraph.aio import Telegraph
from bot import ORIGINAL_BOT_USERNAME, logger

class TELEGRAPH:
    def __init__(self):
        self.telegraph = None
        self.domain = None


    async def initialize(self):
        domain_names = ["telegra.ph", "graph.org"]
        for domain in domain_names:
            try:
                response = requests.get(f"https://{domain}", timeout=3)
                if response.ok:
                    self.domain = domain
                    logger.info(f"Telegraph initialized! Domain: https://{self.domain}")
                    break
            except Exception as e:
                logger.error(e)
        
        if self.domain:
            try:
                self.telegraph = Telegraph(domain=self.domain)
                await self.telegraph.create_account(f"@{ORIGINAL_BOT_USERNAME}")
            except Exception as e:
                logger.error(e)


    async def paste(self, text, username="anonymous"):
        """
        :param text: supports HTML format
        """
        if not (self.domain or self.telegraph):
            logger.error("Telegraph isn't initialized!")
            return
        
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
