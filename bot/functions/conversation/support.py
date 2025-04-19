import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.helper.button_maker import ButtonMaker
from bot.modules.database import MemoryDB

async def conv_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await context.bot.delete_messages(chat.id, [effective_message.id, sent_message.id])
        return
    
    text = (
        "Hey, please send your request/report in one message.\n\n"
        "<blockquote><b>Note:</b> Request/Report should be related to this bot. And we don't provide any support for ban, mute or other things related to groups managed by this bot.</blockquote>"
    )

    btn = ButtonMaker.cbutton([{"Cancel": "conv_cancel"}])
    sent_message = await effective_message.reply_text(text, reply_markup=btn)

    # chat.id is actually userID
    MemoryDB.insert("data_center", chat.id, {"support_message": text, "support_message_id": sent_message.id})

    return "NEXT_STEP"
