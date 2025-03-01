import aiohttp
from bot import logger
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE

async def shortener_url(url):
    shrinkme_api = await LOCAL_DATABASE.get_data("bot_docs", "shrinkme_api")
    if not shrinkme_api:
        shrinkme_api = await MongoDB.get_data("bot_docs", "shrinkme_api")
        if not shrinkme_api:
            logger.error("shrinkme_api not found!")
            return False
    
    try:
        req_url = f"https://shrinkme.io/api?api={shrinkme_api}&url={url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(req_url) as response:
                if response.status != 200:
                    return
                
                data = await response.json()
                shortened_url = data["shortenedUrl"]
                return shortened_url
    except Exception as e:
        logger.error(e)
