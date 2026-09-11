import aiohttp
from app import logger
from app.database import MongoDB


async def ForecastInfo(location: str):
    bot_data = MongoDB.get_bot_data()
    forecast_api = bot_data.get("forecast_api")

    if not forecast_api:
        logger.error("Error: Seem's like forecast_api wasn't provided!")
        return
    
    api_url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": forecast_api,
        "q": location,
        "aqi": "no"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if response.ok:
                    return await response.json()
    except Exception as e:
        logger.error(e)
