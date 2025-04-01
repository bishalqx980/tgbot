from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.database import MemoryDB

async def query_misc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("misc_")

    if query_data == "none":
        await query.answer()
        return

    elif query_data.startswith("broadcast_"):
        # memory access
        data_center = MemoryDB.data_center.get(user.id)
        if not data_center:
            await query.answer("Session Expired.")
            try:
                message_id = query.message.message_id
                await context.bot.delete_messages(user.id, [message_id, message_id - 1])
            except:
                try:
                    await query.delete_message()
                except:
                    pass
            return
        
        # refined query data
        query_data = query_data.removeprefix("broadcast_")

        # accessing datacenter broadcast_data
        broadcast_data = MemoryDB.data_center[user.id]["broadcast"]

        broadcast_update_mapping = {
            "forward_true": {"is_forward": True},
            "forward_false": {"is_forward": False},
            "pin_true": {"is_pin": True},
            "pin_false": {"is_pin": False},
            "done": {"is_done": True},
            "cancel": {"is_cancelled": True}
        }

        if query_data in broadcast_update_mapping:
            broadcast_data.update(broadcast_update_mapping[query_data])
        
        if query_data not in ["done", "cancel"]:
            # formatting message
            text = broadcast_data["text"].format(
                broadcast_data.get("is_forward") or False,
                broadcast_data.get("is_pin") or False
            )

            btn = broadcast_data["btn"]

            await query.edit_message_text(text, reply_markup=btn)
    
    elif query_data.startswith("whisper_"):
        # memory access
        data_center = MemoryDB.data_center.get(chat.id)
        whisper_data = data_center.get("whisper_data") if data_center else None

        if not data_center or not whisper_data:
            await query.answer("Session Expired.")
            try:
                message_id = query.message.message_id
                await context.bot.delete_messages(chat.id, [message_id, message_id - 1])
            except:
                try:
                    await query.delete_message()
                except:
                    pass
            return
        
        whisper_key = query_data.removeprefix("whisper_")
        whisper_user_data = whisper_data.get(whisper_key)

        if not whisper_user_data:
            await query.answer("Whisper Expired.", True)
            try:
                await query.delete_message()
            except:
                pass
            return
        
        whisper_from_user_id = whisper_user_data.get("from_user_id")
        whisper_user_id = whisper_user_data.get("user_id")
        whisper_username = whisper_user_data.get("username") # contains @ prefix
        whisper_message = whisper_user_data.get("message")

        if whisper_from_user_id == user.id:
            # access granted for message sender
            pass

        # verifying user
        elif (whisper_user_id and whisper_user_id != user.id) or (whisper_username and whisper_username != f"@{user.username}"):
            await query.answer("This whisper isn't for you.")
            return
        
        await query.answer(whisper_message, True)
    
    elif query_data == "close":
        try:
            message_id = query.message.message_id
            await context.bot.delete_messages(user.id, [message_id, message_id - 1])
        except:
            try:
                await query.delete_message()
            except:
                pass
        return
