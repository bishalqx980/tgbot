import aiohttp
from app import logger
from app.database import MongoDB


async def ShortURL(url: str):
    bot_data = MongoDB.get_bot_data()
    shrinkme_api = bot_data.get("shrinkme_api")

    if not shrinkme_api:
        logger.error("Error: Seem's like shrinkme_api wasn't provided!")
        return
    
    api_url = "https://shrinkme.io/api"
    params = {
        "api": shrinkme_api,
        "url": url
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if response.ok:
                    data = await response.json()
                    return data.get("shortenedUrl")
    except Exception as e:
        logger.error(e)
