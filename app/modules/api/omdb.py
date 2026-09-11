import aiohttp
from app import logger
from app.database import MongoDB


async def fetch_movieinfo(movie_name: str = None, imdb_id: str = None, year: str = None):
    """
    :param movie_name: requird if `imdb_id` isn't provided
    :param imdb_id: requird if `movie_name` isn't provided
    :param year: optional but recommended if you are using `movie_name`
    """
    bot_data = MongoDB.get_bot_data()
    omdb_api = bot_data.get("omdb_api")
    
    if not omdb_api:
        logger.error("Error: Seem's like omdb_api wasn't provided!")
        return
    
    if movie_name is None and imdb_id is None:
        logger.error("Error: Required parameters wasn't given.")
        return
    
    api_url = "https://omdbapi.com/"
    params = {
        "apikey": omdb_api,
        "t": movie_name, # title
        "i": imdb_id, # imdb_id
        "y": year # year
    }
    
    # filtering out None values
    params = {k: v for k, v in params.items() if v is not None}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if response.ok:
                    return await response.json()
    except Exception as e:
        logger.error(e)
