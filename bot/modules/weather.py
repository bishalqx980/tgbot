import aiohttp
from bot import logger
from bot.utils.database import MemoryDB

async def weather_info(location):
    weather_api = MemoryDB.bot_data.get("weather_api")
    if not weather_api:
        logger.error("weather_api not found!")
        return
    
    api_url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": weather_api,
        "q": location,
        "aqi": "no"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if not response.ok:
                    return

                data = await response.json()
                return data
    except Exception as e:
        logger.error(e)
