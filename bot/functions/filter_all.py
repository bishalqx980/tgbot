async def func_filter_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    msg = update.message.text_html or update.message.caption_html if update.message else None

    if user.id == 777000: # Telegram channel
        return
    
    if chat.type == "private":
        collection_name = "users"
        db_find = user.id
    elif chat.type in ["group", "supergroup"]:
        collection_name = "groups"
        db_find = chat.id
    else:
        collection_name = None
        db_find = None

    find_chat = await LOCAL_DATABASE.find_one(collection_name, db_find)
    if find_chat:
        is_editing = find_chat.get("is_editing") # bool
        if is_editing:
            try:
                msg = int(msg)
            except:
                msg = msg
            
            for key, value in zip(["new_value", "edit_value_del_msg_pointer", "is_editing"], [msg, e_msg, False]):
                await LOCAL_DATABASE.insert_data(collection_name, db_find, {key: value})
            return

    if chat.type == "private" and msg:
        find_user = await LOCAL_DATABASE.find_one("users", user.id)
        if not find_user:
            find_user = await MongoDB.find_one("users", "user_id", user.id)
            if find_user:
                await LOCAL_DATABASE.insert_data("users", user.id, find_user)
            else:
                await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                return
        
        echo_status = find_user.get("echo")
        auto_tr_status = find_user.get("auto_tr")

        if echo_status:
            await Message.reply_msg(update, msg)

        if auto_tr_status:
            lang_code = find_user.get("lang")
            tr_msg = await translate(msg, lang_code)
            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg)
            elif not tr_msg:
                btn_name = ["Language code's"]
                btn_url = ["https://telegra.ph/Language-Code-12-24"]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.", btn)
                return   

    # group's
    elif chat.type in ["group", "supergroup"] and msg:
        _chk_per = await _check_permission(update, user=user, checking_msg=False)
        if not _chk_per:
            return
        
        _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

        if bot_permission.status != ChatMember.ADMINISTRATOR:
            await Message.send_msg(chat.id, "I'm not an admin in this chat!")
            return
        
        find_group = await LOCAL_DATABASE.find_one("groups", chat.id)
        if not find_group:
            find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
            if find_group:
                await LOCAL_DATABASE.insert_data("groups", chat.id, find_group)
            else:
                await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                return
        
        all_links = find_group.get("all_links")
        allowed_links = find_group.get("allowed_links")
        
        if not allowed_links:
            allowed_links = []
        else:
            storage = []
            for i in allowed_links:
                storage.append(i.strip())
            allowed_links = storage

        echo_status = find_group.get("echo")
        auto_tr_status = find_group.get("auto_tr")
        lang_code = find_group.get("lang")
        filters = find_group.get("filters")

        msg_contains_link = False

        if all_links:
            if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                links_list = await RE_LINK.detect_link(msg)
                if links_list:
                    clean_msg = msg
                    allowed_links_count = 0
                    for link in links_list:
                        domain = await RE_LINK.get_domain(link)
                        if domain in allowed_links:
                            allowed_links_count += 1
                        else:
                            if all_links == "delete":
                                clean_msg = clean_msg.replace(link, f"<code>forbidden link</code>")
                            if all_links == "convert":
                                b64_link = await BASE64.encode(link)
                                clean_msg = clean_msg.replace(link, f"<code>{b64_link}</code>")
                    if allowed_links_count != len(links_list):
                        try:
                            clean_msg = f"{user.mention_html()}\n\n{clean_msg}\n\n<i>Delete reason: your message contains forbidden link/s!</i>"
                            await Message.del_msg(chat.id, e_msg)
                            await Message.send_msg(chat.id, clean_msg)
                            msg_contains_link = True
                        except Exception as e:
                            logger.error(e)
        
        if echo_status and not msg_contains_link:
            await Message.reply_msg(update, msg)
        
        if auto_tr_status and not msg_contains_link:
            tr_msg = await translate(msg, lang_code)
            if tr_msg != msg:
                await Message.reply_msg(update, tr_msg)
            elif not tr_msg:
                logger.error(e)
                btn_name = ["Language code's"]
                btn_url = ["https://telegra.ph/Language-Code-12-24"]
                btn = await Button.ubutton(btn_name, btn_url)
                await Message.send_msg(chat.id, "Chat language not found/invalid! Use /settings to set your language.", btn)
        
        if filters:
            for keyword in filters:
                filter_msg = msg.lower() if not isinstance(msg, int) else msg
                if keyword.lower() in filter_msg:
                    filtered_msg = filters[keyword]
                    formattings = {
                        "{first}": user.first_name,
                        "{last}": user.last_name,
                        "{fullname}": user.full_name,
                        "{username}": user.username,
                        "{mention}": user.mention_html(),
                        "{id}": user.id,
                        "{chatname}": chat.title
                    }

                    for key, value in formattings.items():
                        if not value:
                            value = ""
                        filtered_msg = filtered_msg.replace(key, str(value))
                    await Message.reply_msg(update, filtered_msg)