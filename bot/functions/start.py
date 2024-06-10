async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not owner_id:
        msg = f"owner_id: <code>{chat.id}</code>\nPlease add owner_id in <code>config.env</code> file then retry. Otherwise bot won't work properly." if chat.type == "private" else "Error <i>owner_id</i> not provided!"
        await Message.reply_msg(update, msg)
        return
    
    try:
        _bot_info = await bot.get_me()
        _bot = await LOCAL_DATABASE.find("bot_docs")
        if not _bot:
            find = await MongoDB.find("bot_docs", "_id")
            _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
            await LOCAL_DATABASE.insert_data_direct("bot_docs", _bot)

        bot_pic = _bot.get("bot_pic")
        welcome_img = _bot.get("welcome_img")
        support_chat = _bot.get("support_chat")

        msg = (
            f"Hi {user.mention_html()}! I'm <a href='https://t.me/{_bot_info.username}'>{_bot_info.first_name}</a>, your all-in-one bot!\n\n"
            f"<blockquote>Here's a short summary of what I can do:\n\n" # break
            f"• Get response from <b>ChatGPT AI</b>\n"
            f"• Generate image from your prompt\n"
            f"• Download/Search videos from YouTube\n"
            f"• Provide movie information\n"
            f"• Translate languages\n"
            f"• Encode/decode base64\n"
            f"• Shorten URLs\n"
            f"• Ping any URL\n"
            f"• Be your calculator\n"
            f"• Echo your message for fun\n"
            f"• Take website screenshot\n"
            f"• Provide weather information\n"
            f"• <b>Group management</b>\n"
            f"• & Much more...</blockquote>\n\n"
            f"• /help for bot help\n" # break
            f"<i>More Feature coming soon...</i>"
        )

        if _bot_info.username != "MissCiri_bot":
            msg += "\n\nCloned bot of @MissCiri_bot"

        btn_name_1 = ["Add in Group"]
        btn_url_1 = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn_name_2 = ["Developer", "Source Code"]
        btn_url_2 = [f"https://t.me/bishalqx980", "https://github.com/bishalqx980/tgbot"]
        btn_name_3 = ["Support Chat"]
        btn_url_3 = [support_chat]
        btn_1 = await Button.ubutton(btn_name_1, btn_url_1)
        btn_2 = await Button.ubutton(btn_name_2, btn_url_2, True)
        btn = btn_1 + btn_2
        if support_chat:
            try:
                btn_3 = await Button.ubutton(btn_name_3, btn_url_3)
                btn = btn_1 + btn_2 + btn_3
            except Exception as e:
                logger.error(e)
        
        if welcome_img and bot_pic:
            await Message.send_img(user.id, bot_pic, msg, btn)
        else:
            await Message.send_msg(user.id, msg, btn)
        
        find_user = await LOCAL_DATABASE.find_one("users", user.id)
        if not find_user:
            find_user = await MongoDB.find_one("users", "user_id", user.id)
        
        if not find_user:
            data = {
                "user_id": user.id,
                "Name": user.full_name,
                "username": user.username,
                "mention": user.mention_html(),
                "lang": user.language_code,
                "active_status": True
            }
            await MongoDB.insert_single_data("users", data)
            await LOCAL_DATABASE.insert_data("users", user.id, data)
        
        if chat.type != "private":
            _bot_info = await bot.get_me()
            await Message.reply_msg(update, f"Sent in your <a href='http://t.me/{_bot_info.username}'>pm</a>!")
    
    except Forbidden:
        _bot_info = await bot.get_me()
        await Message.reply_msg(update, f"Hola, {user.mention_html()}!\n<a href='http://t.me/{_bot_info.username}'>Start me</a> in pm to chat with me!")
    
    except Exception as e:
        logger.error(e)