import aiohttp
from bot import logger
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE

async def get_movie_info(movie_name=None, imdb_id=None, year=None):
    omdb_api = await LOCAL_DATABASE.get_data("bot_docs", "omdb_api")
    if not omdb_api:
        omdb_api = await MongoDB.get_data("bot_docs", "omdb_api")
        if not omdb_api:
            logger.error("omdb_api not found!")
        return False
    
    if movie_name:
        url = f"https://omdbapi.com/?apikey={omdb_api}&t={movie_name}&y={year}"
    elif imdb_id:
        url = f"https://omdbapi.com/?apikey={omdb_api}&i={imdb_id}"
    else:
        logger.info(f"Movie Name or IMDB ID not provided!!")
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
    except Exception as e:
        logger.error(e)
