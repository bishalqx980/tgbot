import aiohttp
from bot import logger
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE

async def weather_info(location):
    weather_api = await LOCAL_DATABASE.get_data("bot_docs", "weather_api")
    if not weather_api:
        weather_api = await MongoDB.get_data("bot_docs", "weather_api")
        if not weather_api:
            logger.error("weather_api not found!")
            return False
    
    try:
        url = f"https://api.weatherapi.com/v1/current.json?key={weather_api}&q={location}&aqi=no"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return

                data = await response.json()
                return data
    except Exception as e:
        logger.error(e)
