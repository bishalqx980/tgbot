import aiohttp
from bot import logger
from bot.modules.database import MemoryDB

async def weather_info(location):
    weather_api = MemoryDB.bot_data.get("weather_api")
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
