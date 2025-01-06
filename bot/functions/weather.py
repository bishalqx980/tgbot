from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.weather import weather_info


async def func_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = " ".join(context.args)

    if not location:
        await Message.reply_message(update, "Use <code>/weather location_name</code>\nE.g. <code>/weather london</code>")
        return
    
    info = await weather_info(location)
    if info == False:
        await Message.reply_message(update, "weather_api not found!")
        return
    
    if not info:
        await Message.reply_message(update, "Oops, something went wrong...")
        return
    
    loc_name, country, zone, localtime, lastupdate, temp_c, f_temp_c, temp_f, f_temp_f , wind_mph , wind_kph, wind_deg, humidity, uv, condition, condition_icon = info

    msg = (
        f"<b><u>Location info</u></b>\n\n"
        f"<b>City:</b> <code>{loc_name}</code>\n"
        f"<b>Country:</b> <code>{country}</code>\n"
        f"<b>Zone:</b> <code>{zone}</code>\n"
        f"<b>Local time:</b> <code>{localtime}</code>\n\n"
        f"<b><u>Weather info</u></b>\n\n"
        f"<b>Condition:</b> <code>{condition}</code>\n"
        f"<b>Temp (C):</b> <code>{temp_c}</code> <b>feels:</b> <code>{f_temp_c}</code>\n"
        f"<b>Temp (F):</b> <code>{temp_f}</code> <b>feels:</b> <code>{f_temp_f}</code>\n"
        f"<b>Humidity:</b> <code>{humidity}</code>\n\n"
        f"<b>Wind:</b> <code>{wind_mph}</code> | <code>{wind_kph}</code>\n"
        f"<b>Wind (Angle):</b> <code>{wind_deg}</code>\n"
        f"<b>UV Ray:</b> <code>{uv}</code>\n\nNote: <i>⚠ 8 or higher is harmful for skin!</i>"
    )

    await Message.reply_message(update, msg)
