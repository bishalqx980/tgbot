async def func_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = " ".join(context.args)

    if not location:
        await Message.reply_msg(update, "Use <code>/weather location_name</code>\nE.g. <code>/weather london</code>")
        return
    
    info = await weather_info(location)

    if not info:
        await Message.reply_msg(update, "weather_api not found!")
        return
    
    if not info:
        await Message.reply_msg(update, "Something went wrong!")
        return
    
    loc_name = info[0]
    country = info[1]
    zone = info[2]
    localtime = info[3]
    lastupdate = info[4] # last weather update time
    temp_c = info[5]
    f_temp_c = info[6]
    temp_f = info[7]
    f_temp_f = info[8]
    wind_mph = info[9]
    wind_kph = info[10]
    wind_deg = info[11]
    humidity = info[12]
    uv = info[13]
    condition = info[14]
    condition_icon = info[15]
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