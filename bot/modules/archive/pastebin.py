import requests
from bot import logger
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE

POST_URL = "https://pastebin.com/api/api_post.php"

class PASTEBIN:
    async def check_api():
        pastebin_api = await LOCAL_DATABASE.get_data("bot_docs", "pastebin_api")
        if not pastebin_api:
            pastebin_api = await MongoDB.get_data("bot_docs", "pastebin_api")
            if not pastebin_api:
                logger.error("pastebin_api not found!")
                return
        return pastebin_api


    async def create(text):
        check_api = await PASTEBIN.check_api()
        if not check_api:
            return False
        
        data = {
            "api_dev_key": check_api,
            "api_option": "paste",
            "api_paste_code": text,
            # "api_paste_name": title
        }

        try:
            req = requests.post(POST_URL, data)
            return req.text
        except Exception as e:
            logger.error(e)
# To be continued...
