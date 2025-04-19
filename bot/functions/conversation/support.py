from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.button_maker import ButtonMaker

async def conv_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    effective_message = update.effective_message

    text = (
        "Hey, please send your request/report in one message.\n\n"
        "<blockquote><b>Note:</b> Request/Report should be related to this bot. And we don't provide any support for ban, mute or other things related to groups managed by this bot.</blockquote>"
    )

    btn = ButtonMaker.cbutton([{"Cancel": "conv_cancel"}])
    await effective_message.reply_text(text, reply_markup=btn)

    return "NEXT_STEP"
