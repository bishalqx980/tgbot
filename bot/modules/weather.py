import requests
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
        post_url = f"https://api.weatherapi.com/v1/current.json?key={weather_api}&q={location}&aqi=no"
        response = requests.get(post_url)
        weather_data = response.json()
        if weather_data:
            # parents
            location_data = weather_data.get("location")
            current_data = weather_data.get("current")

            # location childs
            loc_name = location_data.get("name")
            loc_country = location_data.get("country")
            loc_tz_id = location_data.get("tz_id") # Asia/Dhaka
            loc_localtime = location_data.get("localtime")

            # current childs
            cur_last_updated = current_data.get("last_updated") # last weather update time
            cur_temp_c = f"{current_data.get('temp_c')}℃" # celsius temp
            cur_f_temp_c = f"{current_data.get('feelslike_c')}℃" # feels like
            cur_temp_f = f"{current_data.get('temp_f')}℉" # fahrenheit temp
            cur_f_temp_f = f"{current_data.get('feelslike_f')}℉" # feels like
            cur_wind_mph = f"{current_data.get('wind_mph')} mph"
            cur_wind_kph = f"{current_data.get('wind_kph')} kph"
            cur_wind_deg = f"{current_data.get('wind_degree')}°"
            cur_humidity = f"{current_data.get('humidity')}%"
            cur_uv = current_data.get("uv") # 11 is dangerous


            # current child > condition childs
            cur_condition_data = current_data.get("condition")
            cur_con_text = cur_condition_data.get("text") # rainy
            cur_con_icon = cur_condition_data.get("icon") # img link

            return loc_name, loc_country, loc_tz_id, loc_localtime, cur_last_updated, cur_temp_c, cur_f_temp_c, cur_temp_f, cur_f_temp_f, cur_wind_mph, cur_wind_kph, cur_wind_deg, cur_humidity, cur_uv, cur_con_text, cur_con_icon
    except Exception as e:
        logger.error(e)
        