import aiohttp
from bot import logger
from bot.modules.database import MemoryDB

async def get_movie_info(movie_name=None, imdb_id=None, year=None):
    omdb_api = MemoryDB.bot_data.get("omdb_api")
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
