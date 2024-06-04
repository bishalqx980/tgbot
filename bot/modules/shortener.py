import requests
from bot import logger
from bot.modules.mongodb import MongoDB

async def shortener_url(url):
    shrinkme_api = await MongoDB.get_data("bot_docs", "shrinkme_api")
    if not shrinkme_api:
        logger.error("shrinkme_api not found!")
        return 0
    
    try:
        post_url = f"https://shrinkme.io/api?api={shrinkme_api}&url={url}"
        response = requests.get(post_url)
        shortened_url = response.json().get("shortenedUrl")
        if shortened_url:
            return shortened_url
    except Exception as e:
        logger.error(e)
