from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helpers.telegram_helper import Message
from bot.modules.database import MemoryDB, MongoDB
from bot.functions.group_management.chat_member_status import _chat_member_status


async def track_bot_chat_act(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    this will check bot status (where it get banned or added or started or blocked etc.)
    """
    chat = update.effective_chat
    my_chat_member = update.my_chat_member
    user = my_chat_member.from_user # cause user

    _chk_stat = await _chat_member_status(my_chat_member) # True means user exist and False is not exist

    if not _chk_stat:
        return
    
    bot_exist, cause = _chk_stat

    if chat.type == "private":
        find_user = MemoryDB.user_data.get(user.id)
        if not find_user:
            find_user = MongoDB.find_one("users", "user_id", user.id)
            if not find_user:
                data = {
                    "user_id": user.id,
                    "name": user.full_name,
                    "username": user.username,
                    "mention": user.mention_html(),
                    "lang": user.language_code
                }
                MongoDB.insert_single_data("users", data)
                MemoryDB.insert_data("user_data", user.id, data)
        
        if bot_exist:
            MongoDB.update_db("users", "user_id", user.id, "active_status", True)
        else:
            MongoDB.update_db("users", "user_id", user.id, "active_status", False)

    elif chat.type in ["group", "supergroup"]:
        find_group = MemoryDB.chat_data.get(chat.id)
        if not find_group:
            find_group = MongoDB.find_one("groups", "chat_id", chat.id)
            if not find_group:
                data = {
                    "chat_id": chat.id,
                    "title": chat.title
                }
                MongoDB.insert_single_data("groups", data)
                MemoryDB.insert_data("chat_data", chat.id, data)
        
        if bot_exist:
            if cause == "JOINED":
                msg = (
                    "Thanks for adding me in this nice chat!\n"
                    "Please make me admin in chat, so I can help you managing this chat effectively!\n"
                    "/help for bot help..."
                )
                # send chat id you effective user
                await Message.send_message(user.id, f"You have added me in {chat.title}\nChatID: <code>{chat.id}</code>")
            elif cause == "PROMOTED":
                msg = (
                    "Thanks for adding me as admin!\n"
                    "Don't forget to checkout /help section..."
                )
            elif cause == "DEMOTED":
                msg = (
                    "Ohh dear, have I done something wrong!\n"
                    "I wish I could help..."
                )
            await Message.send_message(chat.id, msg)
    else:
        if bot_exist and cause == "JOINED":
            await Message.send_message(user.id, f"You have added me in {chat.title}\nChatID: <code>{chat.id}</code>")
