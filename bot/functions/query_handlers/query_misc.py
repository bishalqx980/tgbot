from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.database import MemoryDB

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
        # memory access
        data_center = MemoryDB.data_center.get(chat.id)
        whisper_data = data_center.get("whisper_data") if data_center else None

        if not data_center or not whisper_data:
            await query.answer("Session Expired.", True)
            return
        
        whisper_key = query_data.removeprefix("whisper_")
        whisper_user_data = whisper_data.get(whisper_key)

        if not whisper_user_data:
            await query.answer("Whisper Expired.", True)
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
            await query.answer("This whisper isn't for you.", True)
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
