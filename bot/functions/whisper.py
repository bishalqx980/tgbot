from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button
from bot.modules.group_management.pm_error import _pm_error
from bot.modules.database.local_database import LOCAL_DATABASE


async def func_whisper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = update.message.reply_to_message
    msg = " ".join(context.args)

    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return
    
    if not msg:
        await Message.reply_msg(update, "Use <code>/whisper @mention_user message</code>\nor reply user by <code>/whisper message</code>\nE.g. <code>/whisper @bishalqx980 This is a secret message :)</code>")
        return
    
    await Message.del_msg(chat.id, e_msg)

    if re_msg:
        if re_msg.from_user.is_bot:
            await Message.reply_msg(update, "Whisper isn't for bots...!")
            return
        whisper_user = re_msg.from_user.id
    elif msg:
        msg_split = msg.split()
        whisper_user = msg_split[0]
        msg = " ".join(msg_split[1:])

        if not whisper_user.startswith("@"):
            await Message.reply_msg(update, f"Give a valid username! <code>{whisper_user}</code> is an invalid username!\nor try to reply the user. /whisper for more details...")
            return
        
        # there is a problem > anonymous admin cant read this ...
        if whisper_user.endswith("bot"):
            await Message.reply_msg(update, "Whisper isn't for bots...!")
            return
    
    if len(msg) > 100:
        await Message.reply_msg(update, "Whisper is too long... (max limit 100 character)")
        return

    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "groups",
        "db_find": "chat_id",
        "db_vlaue": chat.id,
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": e_msg.id,
        "edit_data_value_msg_pointer_id": None
    }

    await LOCAL_DATABASE.insert_data("data_center", chat.id, data)

    data = await LOCAL_DATABASE.find_one("data_center", chat.id)
    if data:
        whisper_data = data.get("whisper_data")
        if whisper_data:
            user_whisper_data = whisper_data.get(whisper_user)
            if user_whisper_data:
                await Message.del_msg(chat.id, msg_id=user_whisper_data.get("msg_id"))
    
    data = {
        whisper_user: {
            "whisper_user": whisper_user,
            "whisper_msg": f"{user.first_name}: {msg}",
            "msg_id": e_msg.id + 1
        }
    }

    await LOCAL_DATABASE.insert_data("data_center", chat.id, data, "whisper_data")

    if re_msg:
        whisper_user = re_msg.from_user.mention_html()
    
    msg = f"Hey, {whisper_user} !! You got a message from {user.mention_html()}..."

    btn_name = ["Check the message"]
    btn_data = ["query_whisper"]

    btn = await Button.cbutton(btn_name, btn_data)

    await Message.send_msg(chat.id, msg, btn)
