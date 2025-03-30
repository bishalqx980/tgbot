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

    elif query_data.startswith("broadcast"):
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
    
    elif query_data == "whisper":
        # memory access
        data_center = MemoryDB.data_center.get(chat.id)
        if not data_center:
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
        
        whisper_data = data_center.get("whisper_data")
        if not whisper_data:
            try:
                await query.delete_message()
            except:
                pass
            return
        
        whisper_user_data = whisper_data.get(f"@{user.username}") or whisper_data.get(user.id)

        if not whisper_user_data:
            await query.answer("This whisper isn't for you or whisper has expired!", True)
            return
        
        if whisper_user_data.get("user") not in {user.id, f"@{user.username}"}:
            await query.answer("This whisper isn't for you!", True)
            return
        
        await query.answer(whisper_user_data.get("message"), True)
    
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
