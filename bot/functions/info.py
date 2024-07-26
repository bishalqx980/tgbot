from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.database.mongodb import MongoDB
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users


async def func_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    re_msg = update.message.reply_to_message
    chat_id = " ".join(context.args)

    if re_msg:
        if re_msg.forward_from:
            info_user = re_msg.forward_from
        elif re_msg.from_user:
            if re_msg.from_user.id == user.id:
                await Message.reply_msg(update, "<i>Replied user account is hidden!</i>")
                return
            info_user = re_msg.from_user
    else:
        info_user = user
    
    if chat_id == "db" and re_msg:
        chat_id = info_user.id
    
    if not chat_id:
        msg = (
            f"<b>• Full name:</b> <code>{info_user.full_name}</code>\n"
            f"<b>  » First name:</b> <code>{info_user.first_name}</code>\n"
            f"<b>  » Last name:</b> <code>{info_user.last_name}</code>\n"
            f"<b>• Mention:</b> {info_user.mention_html()}\n"
            f"<b>• Username:</b> @{info_user.username}\n"
            f"<b>• ID:</b> <code>{info_user.id}</code>\n"
            f"<b>• Lang:</b> <code>{info_user.language_code}</code>\n"
            f"<b>• Is bot:</b> <code>{info_user.is_bot}</code>\n"
            f"<b>• Is premium:</b> <code>{info_user.is_premium}</code>"
        )

        await Message.reply_msg(update, msg)
        return
    
    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "Access denied!")
        return

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
            "welcome_user",
            "farewell_user",
            "antibot",
            "del_cmd",
            "all_links",
            "allowed_links",
            "log_channel",
            "filters",
            "custom_welcome_msg"
        ]

        msg = "<b><u>Database info</u></b>\n\n"
        
        for key in entries:
            data = find_group.get(key)
            if data:
                if key == "allowed_links":
                    data = ", ".join(data)
                elif key == "filters":
                    data = "\n".join(f"» {i}" for i in data)
            
            if key in ["filters", "custom_welcome_msg"]:
                msg += f"<b>{key}</b>:\n<pre>{data}</pre>\n"
            else: 
                msg += f"<b>{key}</b>: <code>{data}</code>\n"

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

        msg = "<b><u>Database info</u></b>\n\n"
        
        for key in entries:
            data = find_user.get(key)
            if key in ["username", "mention"]:
                if key == "username":
                    msg += f"<b>{key}</b>: @{data}\n"
                else:
                    msg += f"<b>{key}</b>: {data}\n"
            else:
                msg += f"<b>{key}</b>: <code>{data}</code>\n"
        
        await Message.reply_msg(update, msg)
