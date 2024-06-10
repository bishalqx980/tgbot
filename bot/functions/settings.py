async def func_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message

    _bot = await LOCAL_DATABASE.find("bot_docs")
    if not _bot:
        find = await MongoDB.find("bot_docs", "_id")
        _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
        await LOCAL_DATABASE.insert_data_direct("bot_docs", _bot)

    if chat.type == "private":
        find_user = await LOCAL_DATABASE.find_one("users", user.id)
        if not find_user:
            find_user = await MongoDB.find_one("users", "user_id", user.id)
            if find_user:
                await LOCAL_DATABASE.insert_data("users", user.id, find_user)
            else:
                await Message.reply_msg(update, "User data not found! Block me then start me again! (no need to delete chat)")
                return
        
        user_mention = find_user.get("mention")
        lang = find_user.get("lang")
        echo = find_user.get("echo")
        auto_tr = find_user.get("auto_tr")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"• User: {user_mention}\n"
            f"• ID: <code>{user.id}</code>\n\n"

            f"• Lang: <code>{lang}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Auto tr: <code>{auto_tr}</code>\n\n"
        )

        btn_name_row1 = ["Language", "Auto translate"]
        btn_data_row1 = ["lang", "auto_tr"]

        btn_name_row2 = ["Echo", "Close"]
        btn_data_row2 = ["set_echo", "close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)

        btn = row1 + row2

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
            await Message.send_img(chat.id, image, msg, btn)
        except Exception as e:
            logger.error(e)
            try:
                image = await LOCAL_DATABASE.get_data("bot_docs", "bot_pic")
                if not image:
                    image = await MongoDB.get_data("bot_docs", "bot_pic")
                await Message.send_img(chat.id, image, msg, btn)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat.id, msg, btn)

    elif chat.type in ["group", "supergroup"]:
        await _check_del_cmd(update, context)

        if user.is_bot:
            await Message.reply_msg(update, "I don't take permission from anonymous admins!")
            return

        _chk_per = await _check_permission(update, user=user)

        if not _chk_per:
            return
        
        _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per
            
        if bot_permission.status != ChatMember.ADMINISTRATOR:
            await Message.reply_msg(update, "I'm not an admin in this chat!")
            return
    
        if not bot_permission.can_change_info:
            await Message.reply_msg(update, "I don't have enough rights to manage this chat!")
            return
        
        if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            await Message.reply_msg(update, "You aren't an admin in this chat!")
            return
        
        if user_permission.status == ChatMember.ADMINISTRATOR:
            if not admin_rights.get("can_change_info"):
                await Message.reply_msg(update, "You don't have enough rights to manage this chat!")
                return

        
        find_group = await LOCAL_DATABASE.find_one("groups", chat.id)
        if not find_group:
            find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
            if find_group:
                await LOCAL_DATABASE.insert_data("groups", chat.id, find_group)
            else:
                await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                return
        
        title = find_group.get("title")
        lang = find_group.get("lang")

        echo = find_group.get("echo")
        auto_tr = find_group.get("auto_tr")
        welcome_msg = find_group.get("welcome_msg")
        goodbye_msg = find_group.get("goodbye_msg")
        antibot = find_group.get("antibot")
        ai_status = find_group.get("ai_status")
        del_cmd = find_group.get("del_cmd")
        all_links = find_group.get("all_links")
        allowed_links = find_group.get("allowed_links")
        if allowed_links:
            storage, counter = "", 0
            for i in allowed_links:
                counter += 1
                if counter == len(allowed_links):
                    storage += f"{i}"
                else:
                    storage += f"{i}, "
            allowed_links = storage
        
        log_channel = find_group.get("log_channel")

        msg = (
            "<u><b>Chat Settings</b></u>\n\n"
            f"• Title: {title}\n"
            f"• ID: <code>{chat.id}</code>\n\n"

            f"• Lang: <code>{lang}</code>\n"
            f"• Echo: <code>{echo}</code>\n"
            f"• Auto tr: <code>{auto_tr}</code>\n"
            f"• Welcome user: <code>{welcome_msg}</code>\n"
            f"• Goodbye user: <code>{goodbye_msg}</code>\n"
            f"• Antibot: <code>{antibot}</code>\n"
            f"• AI status: <code>{ai_status}</code>\n"
            f"• Delete cmd: <code>{del_cmd}</code>\n"
            f"• All links: <code>{all_links}</code>\n"
            f"• Allowed links: <code>{allowed_links}</code>\n"
            f"• Log channel: <code>{log_channel}</code>\n"
        )

        btn_name_row1 = ["Language", "Auto translate"]
        btn_data_row1 = ["lang", "auto_tr"]

        btn_name_row2 = ["Echo", "Anti bot"]
        btn_data_row2 = ["set_echo", "antibot"]

        btn_name_row3 = ["Welcome", "Goodbye"]
        btn_data_row3 = ["welcome_msg", "goodbye_msg"]

        btn_name_row4 = ["Delete cmd", "Log channel"]
        btn_data_row4 = ["del_cmd", "log_channel"]

        btn_name_row5 = ["Links", "AI"]
        btn_data_row5 = ["links_behave", "ai_status"]

        btn_name_row6 = ["Close"]
        btn_data_row6 = ["close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
        row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)
        row4 = await Button.cbutton(btn_name_row4, btn_data_row4, True)
        row5 = await Button.cbutton(btn_name_row5, btn_data_row5, True)
        row6 = await Button.cbutton(btn_name_row6, btn_data_row6)

        btn = row1 + row2 + row3 + row4 + row5 + row6

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
            await Message.send_img(chat.id, image, msg, btn)
        except Exception as e:
            logger.error(e)
            try:
                image = await LOCAL_DATABASE.get_data("bot_docs", "bot_pic")
                if not image:
                    image = await MongoDB.get_data("bot_docs", "bot_pic")
                await Message.send_img(chat.id, image, msg, btn)
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat.id, msg, btn)