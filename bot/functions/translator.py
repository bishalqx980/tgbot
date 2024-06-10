async def func_translator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message
    msg = re_msg.text_html or re_msg.caption_html if re_msg else None
    input_text = " ".join(context.args)

    if not msg and not input_text:
        btn_name = ["Language code's"]
        btn_url = ["https://telegra.ph/Language-Code-12-24"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.reply_msg(update, "Use <code>/tr text</code> or <code>/tr lang_code text</code> or reply the text with <code>/tr</code> or <code>/tr lang_code</code>\n\nEnable auto translator mode for this chat from /settings", btn)
        return
    
    to_translate = None
    lang_code = None
    
    if input_text:
        words = input_text.split()
        first_word = words[0]
        if first_word in LANG_CODE_LIST:
            lang_code = first_word
            to_translate = " ".join(words[1:])
    
    if not msg and not to_translate and input_text: # /tr text and lang_code = get from db
        to_translate = input_text
    
    if msg and not to_translate: # /tr (maybe lang_code or maybe not) and replied
        to_translate = msg
    
    if not lang_code:
        if chat.type == "private":
            find_user = await LOCAL_DATABASE.find_one("users", user.id)
            if not find_user:
                find_user = await MongoDB.find_one("users", "user_id", user.id)
                if find_user:
                    await LOCAL_DATABASE.insert_data("users", user.id, find_user)
                else:
                    await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    return
            
            lang_code = find_user.get("lang")
        else:
            find_group = await LOCAL_DATABASE.find_one("groups", chat.id)
            if not find_group:
                find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
                if find_group:
                    await LOCAL_DATABASE.insert_data("groups", chat.id, find_group)
                else:
                    await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                    return
            
            lang_code = find_group.get("lang")

    tr_msg = await translate(to_translate, lang_code)
    if tr_msg:
        sent_msg = await Message.reply_msg(update, tr_msg)
        if not sent_msg:
            await Message.reply_msg(update, "Oops, internal problem occurred...")

    if not tr_msg:
        _bot = await LOCAL_DATABASE.find("bot_docs")
        if not _bot:
            find = await MongoDB.find("bot_docs", "_id")
            _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
            await LOCAL_DATABASE.insert_data_direct("bot_docs", _bot)
        
        btn_name = ["Language code's"]
        btn_url = ["https://telegra.ph/Language-Code-12-24"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.", btn)
        return