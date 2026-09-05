from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot import TTS_LANG_CODES_URL
from bot.modules.gtts import text_to_speech


async def func_tts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    lang_code = " ".join(context.args) or "en"

    if not re_msg:
        return await effective_message.reply_text(
            "Reply any text to convert it into a voice message! E.g. Reply any message with <code>/tts en</code> to get english accent voice.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Language code's", TTS_LANG_CODES_URL)
            ]])
        )
    
    sent_message = await effective_message.reply_text("Processing...")

    response = text_to_speech(re_msg.text or re_msg.caption, lang_code)
    if not response:
        return await sent_message.edit_text(
            "Oops! Something went wrong!"
        )
    
    file_name = f"Voice {re_msg.id} [ {lang_code} ].mp3"

    await sent_message.delete()
    await effective_message.reply_audio(response, title=file_name, filename=file_name)
