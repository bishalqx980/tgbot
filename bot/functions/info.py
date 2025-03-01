from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import MessageOriginType
from bot.modules.database.mongodb import MongoDB
from bot.helper.telegram_helper import Message, Button
from bot.functions.power_users import _power_users


async def func_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message
    chat_id = " ".join(context.args)
    victim = None

    if re_msg:
        forward_origin = re_msg.forward_origin
        from_user = re_msg.from_user
    
        if forward_origin and forward_origin.type == MessageOriginType.USER:
            victim = forward_origin.sender_user
        
        if from_user and not forward_origin:
            victim = from_user
        
        if not victim:
            await Message.reply_message(update, f"<b>• Full name:</b> <code>{forward_origin.sender_user_name}</code>\n<i>Replied user account is hidden!</i>")
            return
    else:
        victim = user
    
    if chat_id == "db" and re_msg:
        chat_id = victim.id
    
    if not chat_id:
        victim_photos = await victim.get_profile_photos()
        victim_pfp = None
        if victim_photos.photos:
            victim_pfp = victim_photos.photos[0][-1].file_id # returns victims latest pfp file id
        
        victim_username = f"@{victim.username}" if victim.username else None
        msg = (
            f"<b>• Full name:</b> <code>{victim.full_name}</code>\n"
            f"<b>  » First name:</b> <code>{victim.first_name}</code>\n"
            f"<b>  » Last name:</b> <code>{victim.last_name}</code>\n"
            f"<b>• Mention:</b> {victim.mention_html()}\n"
            f"<b>• Username:</b> {victim_username}\n"
            f"<b>• ID:</b> <code>{victim.id}</code>\n"
            f"<b>• Lang:</b> <code>{victim.language_code}</code>\n"
            f"<b>• Is bot:</b> <code>{victim.is_bot}</code>\n"
            f"<b>• Is premium:</b> <code>{victim.is_premium}</code>"
        )

        btn = await Button.ubutton({"User Profile": f"tg://user?id={victim.id}"}) if victim.username else None

        if victim_pfp:
            await Message.reply_image(update, victim_pfp, msg, btn=btn)
        else:
            await Message.reply_message(update, msg, btn=btn)
        return
    
    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_message(update, "Access denied!")
        return

    if "-100" in str(chat_id):
        find_group = await MongoDB.find_one("groups", "chat_id", int(chat_id))
        if not find_group:
            await Message.reply_message(update, "Chat not found!")
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

        await Message.reply_message(update, msg)
    else:
        find_user = await MongoDB.find_one("users", "user_id", int(chat_id))
        if not find_user:
            await Message.reply_message(update, "User not found!")
            return
        
        entries = [
            "name",
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
                    data = f"@{data}" if data else None
                    msg += f"<b>{key}</b>: {data}\n"
                else:
                    msg += f"<b>{key}</b>: {data}\n"
            else:
                msg += f"<b>{key}</b>: <code>{data}</code>\n"
        
        await Message.reply_message(update, msg)
