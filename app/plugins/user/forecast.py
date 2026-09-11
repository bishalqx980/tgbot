from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.helpers import CommandArgs
from app.modules.api.weatherforecast import ForecastInfo


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "weather-forecast",
    "commands": ["weather", "forecast"], # list of commands including aliases

    "description": "Get forecast information for specified location! E.g. `/forecast london`",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Forecast", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    location = CommandArgs(message.text, message.command)

    if not location:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"
    
            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"
    
            f"#{__module__['_id']}"
        )
    
    forecast_info = await ForecastInfo(location)

    if not forecast_info:
        return await message.reply(
            "Error: Something went wrong! Invalid location name?"
        )
    
    await message.reply(
        f"> **Location info**\n\n"

        f"**City:** `{forecast_info['location']['name']}`\n"
        f"**Country:** `{forecast_info['location']['country']}`\n"
        f"**Zone:** `{forecast_info['location']['tz_id']}`\n"
        f"**Local time:** `{forecast_info['location']['localtime']}`\n\n"

        f"> **Weather info**\n\n"

        f"**Condition:** `{forecast_info['current']['condition']['text']}`\n"
        f"**Temp (C):** `{forecast_info['current']['temp_c']}℃` **feels:** `{forecast_info['current']['feelslike_c']}℃`\n"
        f"**Temp (F):** `{forecast_info['current']['temp_f']}℉` **feels:** `{forecast_info['current']['feelslike_f']}℉`\n"
        f"**Humidity:** `{forecast_info['current']['humidity']}%`\n\n"

        f"**Wind:** `{forecast_info['current']['wind_mph']}mph` | `{forecast_info['current']['wind_kph']}kph`\n"
        f"**Wind (Angle):** `{forecast_info['current']['wind_degree']}°`\n"
        f"**UV Ray:** `{forecast_info['current']['uv']}`\n\n"

        "> **Note:** ⚠ 8 or higher is harmful for skin!"
    )
