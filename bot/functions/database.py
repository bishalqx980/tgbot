async def func_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    chat_id = " ".join(context.args)

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    if chat_id:
        if "-100" in str(chat_id):
            find_group = await MongoDB.find_one("groups", "chat_id", int(chat_id))
            if not find_group:
                await Message.reply_msg(update, "Chat not found!")
                return
            
            title = find_group.get("title")
            chat_id = find_group.get("chat_id")
            lang = find_group.get("lang")
            echo = find_group.get("echo")
            auto_tr = find_group.get("auto_tr")
            welcome_msg = find_group.get("welcome_msg")
            custom_welcome_msg = find_group.get("custom_welcome_msg")
            goodbye_msg = find_group.get("goodbye_msg")
            antibot = find_group.get("antibot")
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
            filters = find_group.get("filters")
            if filters:
                storage = ""
                for key in filters:
                    storage += f"» {key}: {filters[key]}\n"

            msg = (
                f"<code>Title         :</code> {title}\n"
                f"<code>ID            :</code> <code>{chat_id}</code>\n"
                f"<code>Lang          :</code> {lang}\n"
                f"<code>Echo          :</code> {echo}\n"
                f"<code>Auto tr       :</code> {auto_tr}\n"
                f"<code>Welcome       :</code> {welcome_msg}\n"
                f"<blockquote>{custom_welcome_msg}</blockquote>\n"
                f"<code>Farewell      :</code> {goodbye_msg}\n"
                f"<code>Antibot       :</code> {antibot}\n"
                f"<code>Delete cmd    :</code> {del_cmd}\n"
                f"<code>All links     :</code> {all_links}\n"
                f"<code>Allowed links:</code> {allowed_links}\n"
                f"<code>Log channel   :</code> <code>{log_channel}</code>\n"
                f"<code>Filters       :</code> <blockquote>{storage}</blockquote>\n"
            )
            await Message.reply_msg(update, f"<b>{msg}</b>")
        else:
            find_user = await MongoDB.find_one("users", "user_id", int(chat_id))
            if not find_user:
                await Message.reply_msg(update, "User not found!")
                return
            
            Name = find_user.get("Name")
            user_id = find_user.get("user_id")
            username = find_user.get("username")
            mention = find_user.get("mention")
            lang = find_user.get("lang")
            echo = find_user.get("echo")
            active_status = find_user.get("active_status")

            msg = (
                f"<code>Name     :</code> {Name}\n"
                f"<code>Mention  :</code> {mention}\n"
                f"<code>ID       :</code> <code>{user_id}</code>\n"
                f"<code>Username :</code> @{username}\n"
                f"<code>Lang     :</code> {lang}\n"
                f"<code>Echo     :</code> {echo}\n"
                f"<code>A. status:</code> {active_status}\n"
            )
            await Message.reply_msg(update, f"<b>{msg}</b>")
        return
    
    db = await MongoDB.info_db()
    msg = "▬▬▬▬▬▬▬▬▬▬\n"
    for info in db:
        msg += (
            f"<code>Doc name   :</code> {info[0]}\n"
            f"<code>Doc count  :</code> {info[1]}\n"
            f"<code>Doc size   :</code> {info[2]}\n"
            f"<code>Actual size:</code> {info[3]}\n"
            f"▬▬▬▬▬▬▬▬▬▬\n"
        )
    active_status = await MongoDB.find("users", "active_status")
    active_users = active_status.count(True)
    inactive_users = active_status.count(False)
    await Message.reply_msg(update, f"<b>{msg}Active users: {active_users}\nInactive users: {inactive_users}</b>")