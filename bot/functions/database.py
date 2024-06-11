from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.database.mongodb import MongoDB
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users


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
            
            entries = [
                "title",
                "chat_id",
                "lang",
                "echo",
                "auto_tr",
                "welcome_msg",
                "custom_welcome_msg",
                "goodbye_msg",
                "antibot",
                "del_cmd",
                "all_links",
                "allowed_links",
                "log_channel",
                "filters"
            ]

            msg = ""
            
            for key in entries:
                data = find_group.get(key)

                if key == "allowed_links":
                    storage, counter = "", 0
                    for i in data:
                        counter += 1
                        if counter == len(data):
                            storage += f"{i}"
                        else:
                            storage += f"{i}, "
                    data = storage

                if key == "filters":
                    storage = ""
                    for i in data:
                        storage += f"» {i}\n"
                    data = storage
                
                msg += f"<b>{key}</b>: {data}\n"

            await Message.reply_msg(update, msg)
        else:
            find_user = await MongoDB.find_one("users", "user_id", int(chat_id))
            if not find_user:
                await Message.reply_msg(update, "User not found!")
                return
            
            entries = [
                "Name",
                "user_id",
                "username",
                "mention",
                "lang",
                "echo",
                "active_status"
            ]

            msg = ""
            
            for key in entries:
                data = find_group.get(key)
                msg += f"<b>{key}</b>: {data}\n"
            
            await Message.reply_msg(update, msg)
    else:
        db = await MongoDB.info_db()
        msg = "<b>⋰⋰⋰⋰⋰⋰⋰⋰⋰⋰</b>\n"
        for info in db:
            msg += (
                f"<b>Name</b>: <code>{info[0]}</code>\n"
                f"<b>Count</b>: <code>{info[1]}</code>\n"
                f"<b>Size</b>: <code>{info[2]}</code>\n"
                f"<b>A. size</b>: <code>{info[3]}</code>\n"
                f"<b>⋰⋰⋰⋰⋰⋰⋰⋰⋰⋰</b>\n"
            )
        active_status = await MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)
        await Message.reply_msg(update, f"{msg}<b>Active users</b>: <code>{active_users}</code>\n<b>Inactive users</b>: <code>{inactive_users}</code>")
