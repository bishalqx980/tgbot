async def func_bsettings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    btn_name_row1 = ["Bot pic", "Welcome img"]
    btn_data_row1 = ["bot_pic", "welcome_img"]

    btn_name_row2 = ["Images", "Support chat"]
    btn_data_row2 = ["images", "support_chat"]

    btn_name_row3 = ["GitHub", "Server url", "Sudo"]
    btn_data_row3 = ["github_repo", "server_url", "sudo_users"]

    btn_name_row4 = ["Shrinkme API", "OMDB API", "Weather API"]
    btn_data_row4 = ["shrinkme_api", "omdb_api", "weather_api"]

    btn_name_row5 = ["⚠ Restore Settings", "Close"]
    btn_data_row5 = ["restore_db", "close"]

    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
    row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
    row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
    row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)

    btn = row1 + row2 + row3 + row4 + row5

    try:
        images = LOCAL_DATABASE.get_data("bot_docs", "images")
        if not images:
            images = await MongoDB.get_data("bot_docs", "images")
        
        if images:
            image = random.choice(images).strip()
        else:
            image = await LOCAL_DATABASE.get_data("bot_docs", "bot_pic")
            if not image:
                image = await MongoDB.get_data("bot_docs", "bot_pic")
        await Message.send_img(chat.id, image, "<u><b>Bot Settings</b></u>", btn)
    except Exception as e:
        logger.error(e)
        try:
            image = await LOCAL_DATABASE.get_data("bot_docs", "bot_pic")
            if not image:
                image = await MongoDB.get_data("bot_docs", "bot_pic")
            await Message.send_img(chat.id, image, "<u><b>Bot Settings</b></u>", btn)
        except Exception as e:
            logger.error(e)
            await Message.send_msg(chat.id, "<u><b>Bot Settings</b></u>", btn)