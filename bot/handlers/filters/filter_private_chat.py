from telegram import Update, ReactionTypeEmoji
from telegram.ext import ContextTypes
from telegram.error import Forbidden

from bot import TL_LANG_CODES_URL, config
from bot.helpers import BuildKeyboard
from bot.utils.database import DBConstants, database_search

from .edit_database import edit_database
from .auto_translate import autoTranslate

async def filter_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    # Support Seekers Reply
    if user.id in [config.owner_id] and message.reply_to_message:
        replied_message = message.reply_to_message
        if "#support" in replied_message.text:
            support_seeker_id = replied_message.text.split("#id")[1].strip()
            # sending message to support seeker
            try:
                await context.bot.send_message(support_seeker_id, message.text_html)
                reaction = "👍"
            except Forbidden:
                reaction = "👎"
            except:
                reaction = "🤷‍♂"
            # Confirm support team that message is sent or not
            await message.set_reaction([ReactionTypeEmoji(reaction)])
    
    is_editing = edit_database(chat.id, user.id, message)
    if is_editing:
        return
    
    user_data = database_search(DBConstants.USERS_DATA, "user_id", user.id)
    if not user_data:
        await message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return
    
    # Echo message
    if user_data.get("echo"):
        await message.reply_text(message.text_html or message.caption_html)
    
    # Auto Translator
    auto_tr = user_data.get("auto_tr")
    chat_lang = user_data.get("lang")

    if auto_tr and not chat_lang:
        btn = BuildKeyboard.ubutton([{"Language code's": TL_LANG_CODES_URL}])
        await message.reply_text("Chat language code wasn't found! Use /settings to set chat language.", reply_markup=btn)
    
    elif auto_tr:
        await autoTranslate(message, user, chat_lang)
