from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.database.common import database_search

async def query_misc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("misc_")

    if query_data == "none":
        await query.answer()
        return
    
    elif query_data.startswith("whisper_"):
        chat_data = database_search("chats_data", "chat_id", chat.id)
        if not chat_data:
            await query.answer("Chat isn't registered! Remove/Block me from this chat then add me again!", True)
            return
        
        whispers = chat_data.get("whispers") or {}
        # other variables
        whisper_key = query_data.removeprefix("whisper_")
        whisper_user_data = whispers.get(whisper_key)

        if not whisper_user_data:
            await query.answer("What? There is no whisper message!!", True)
            return
        
        whisper_sender_user_id = whisper_user_data.get("sender_user_id")
        whisper_user_id = whisper_user_data.get("user_id")
        whisper_username = whisper_user_data.get("username") # contains @ prefix
        whisper_message = whisper_user_data.get("message")

        if whisper_sender_user_id == user.id:
            # access granted for message sender
            pass

        # verifying user
        elif (whisper_user_id and whisper_user_id != user.id) or (whisper_username and whisper_username != user.name):
            await query.answer("This whisper isn't for you. (if you believe it's yours then maybe you changed your `username`)", True)
            return
        
        await query.answer(whisper_message, True)
    
    elif query_data == "close":
        try:
            message_id = query.message.message_id
            await chat.delete_messages([message_id, message_id - 1])
        except:
            try:
                await query.delete_message()
            except:
                pass
