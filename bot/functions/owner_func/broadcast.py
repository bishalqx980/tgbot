import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.helper import BuildKeyboard
from bot.modules.database import MemoryDB
from ..sudo_users import fetch_sudos

class BroadcastMenu:
    TEXT = (
        "<blockquote><b>Broadcast</b></blockquote>\n\n"

        "Media: <code>{}</code>\n"
        "Message: <code>{}</code>\n"
        "Pin: <code>{}</code>"
    )

    BUTTONS = [
        {"Media 📸": "broadcast_add_media", "See 👀": "broadcast_see_media"},
        {"Text 📝": "broadcast_add_text", "See 👀": "broadcast_see_text"},
        {"Pin 📌": "broadcast_value_pin"},
        {"Full preview 👀": "broadcast_preview"},
        {"Done": "broadcast_sendToAll", "Cancel": "broadcast_close"}
    ]


async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    sudo_users = fetch_sudos()
    if user.id not in sudo_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await chat.delete_messages([effective_message.id, sent_message.id])
        return
    
    # storing required data in datacenter
    data = {
        "user_id": user.id, # authorization
        "broadcast": {
            "media": None,
            "text": None,
            "pin": False,
            "is_cancelled": False
        }
    }

    MemoryDB.insert("data_center", chat.id, data)
    # accessing memory data
    broadcast_data = MemoryDB.data_center[chat.id]["broadcast"]

    text = BroadcastMenu.TEXT.format(
        "Available" if broadcast_data["media"] else "Not available",
        "Available" if broadcast_data["text"] else "Not available",
        broadcast_data["pin"]
    )
    
    btn = BuildKeyboard.cbutton(BroadcastMenu.BUTTONS)
    await effective_message.reply_text(text, reply_markup=btn)
