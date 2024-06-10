from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.weather import weather_info


async def func_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = " ".join(context.args)

    if not location:
        await Message.reply_msg(update, "Use <code>/weather location_name</code>\nE.g. <code>/weather london</code>")
        return
    
    info = await weather_info(location)

    if info == 0:
        await Message.reply_msg(update, "weather_api not found!")
        return
    
    if not info:
        await Message.reply_msg(update, "Something went wrong!")
        return
    
    loc_name, country, zone, localtime, lastupdate, temp_c, f_temp_c, temp_f, f_temp_f , wind_mph , wind_kph, wind_deg, humidity, uv, condition, condition_icon = info

    msg = (
        f"<b>|———LOCATION INFO———|</b>\n\n"
        f"City: <code>{loc_name}</code>\n"
        f"Country: <code>{country}</code>\n"
        f"Zone: <code>{zone}</code>\n"
        f"Local Time: <code>{localtime}</code>\n\n"
        f"<b>|———WEATHER INFO———|</b>\n\n"
        f"➠ {condition} ✨\n\n"
        f"<b>➲ Temperature info</b>\n"
        f"temp (C) » <code>{temp_c}</code>\nFeels » <code>{f_temp_c}</code>\n"
        f"temp (F) » <code>{temp_f}</code>\nFeels » <code>{f_temp_f}</code>\n"
        f"Humidity: <code>{humidity}</code>\n\n"
        f"Wind: <code>{wind_mph}</code> | <code>{wind_kph}</code>\n"
        f"Wind `Angle`: <code>{wind_deg}</code>\n"
        f"UV Ray: <code>{uv}</code>\n\n<pre>⚠ 8 or higher is harmful for skin!</pre>"
    )

    await Message.reply_msg(update, msg)
