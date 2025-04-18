from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.button_maker import ButtonMaker
from bot.modules.gtts import text_to_speech

async def func_tts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    lang_code = " ".join(context.args) or "en"

    if not re_msg:
        btn = ButtonMaker.ubutton([{"Language code's": "https://telegra.ph/Text-to-speech---language-codes-tts-01-23"}])
        await effective_message.reply_text("Reply any text to convert it into a voice message! E.g. Reply any message with <code>/tts en</code> to get english accent voice.", reply_markup=btn)
        return
    
    sent_message = await effective_message.reply_text("Processing...")

    response = text_to_speech(re_msg.text or re_msg.caption, lang_code)
    if not response:
        await context.bot.edit_message_text("Oops! Something went wrong!", chat.id, sent_message.id)
        return
    
    file_name = f"Voice {re_msg.id} [ {lang_code} ].mp3"

    await context.bot.delete_message(chat.id, sent_message.id)
    await effective_message.reply_audio(response, title=file_name, filename=file_name)
