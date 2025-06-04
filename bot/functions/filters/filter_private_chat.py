from telegram import Update
from telegram.ext import ContextTypes
from bot import TL_LANG_CODES_URL
from bot.helper.keyboard_builder import ButtonMaker
from bot.modules.database.common import database_search
from bot.modules.translator import translate
from .edit_database import edit_database

async def filter_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    is_editing = edit_database(chat.id, user.id, effective_message.text, effective_message.id)
    if is_editing:
        return
    
    user_data = database_search("users_data", "user_id", user.id)
    if not user_data:
        await effective_message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return
    
    echo_status = user_data.get("echo")
    auto_tr_status = user_data.get("auto_tr")

    if echo_status:
        await effective_message.reply_text(effective_message.text_html or effective_message.caption_html)

    if auto_tr_status:
        lang_code = user_data.get("lang")
        if lang_code:
            original_text = effective_message.text or effective_message.caption
            translated_text = translate(original_text, lang_code)

            if translated_text and translated_text.lower() != original_text.lower():
                await effective_message.reply_text(translated_text)
            
            elif translated_text == False:
                btn = ButtonMaker.ubutton([{"Language code's": TL_LANG_CODES_URL}])
                await effective_message.reply_text("Invalid language code was given! Use /settings to set chat language.", reply_markup=btn)
        else:
            btn = ButtonMaker.ubutton([{"Language code's": TL_LANG_CODES_URL}])
            await effective_message.reply_text("Chat language code wasn't found! Use /settings to set chat language.", reply_markup=btn)
