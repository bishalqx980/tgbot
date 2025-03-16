from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.modules.database import MemoryDB, MongoDB
from bot.functions.group_management.auxiliary.chat_member_status import chat_member_status

async def bot_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message
    my_chat_member = update.my_chat_member
    cause_user = my_chat_member.from_user

    member_status = chat_member_status(my_chat_member) # True means user exist and False is not exist
    if not member_status:
        return
    
    is_bot_exist, cause = member_status

    if chat.type == ChatType.PRIVATE:
        find_user = MemoryDB.user_data.get(cause_user.id)
        if not find_user:
            find_user = MongoDB.find_one("users", "user_id", cause_user.id)
            if not find_user:
                data = {
                    "user_id": cause_user.id,
                    "name": cause_user.full_name,
                    "username": cause_user.username,
                    "mention": cause_user.mention_html(),
                    "lang": cause_user.language_code
                }
                MongoDB.insert_single_data("users", data)
                MemoryDB.insert_data("user_data", cause_user.id, data)
        
        if is_bot_exist:
            MongoDB.update_db("users", "user_id", cause_user.id, "active_status", True)
        else:
            MongoDB.update_db("users", "user_id", cause_user.id, "active_status", False)

    elif chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
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
        
        if is_bot_exist:
            if cause == "JOINED":
                text = (
                    "Thanks for adding me in this nice chat!\n"
                    "Please make me admin in chat, so I can help you managing this chat effectively!\n"
                    "/help for bot help..."
                )

                # send message to user.id
                await context.bot.send_message(cause_user.id, f"You have added me in {chat.title}\nChatID: <code>{chat.id}</code>")

            elif cause == "PROMOTED":
                text = (
                    "Thanks for adding me as admin!\n"
                    "Don't forget to checkout /help section..."
                )

            elif cause == "DEMOTED":
                text = (
                    "Ohh dear, have I done something wrong!\n"
                    "I wish I could help..."
                )

            await effective_message.reply_text(text)
    
    elif is_bot_exist and cause == "JOINED":
        await context.bot.send_message(cause_user.id, f"You have added me in {chat.title}\nChatID: <code>{chat.id}</code>")
