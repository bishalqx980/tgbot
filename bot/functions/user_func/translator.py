from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database.common import database_search
from bot.modules.translator import fetch_lang_codes, translate

async def func_tr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    text = (re_msg.text or re_msg.caption) if re_msg else None
    context_args = " ".join(context.args)

    if not text and not context_args:
        btn = ButtonMaker.ubutton([{"Language code's": "https://telegra.ph/Language-Code-12-24"}])
        await effective_message.reply_text("Use <code>/tr text</code> or <code>/tr lang code text</code> or reply the text with <code>/tr</code> or <code>/tr lang code</code>\n\nEnable auto translator mode for this chat from /settings", reply_markup=btn)
        return
    
    to_translate = None
    lang_code = None
    LANG_CODE_LIST = fetch_lang_codes()
    
    if context_args:
        words = context_args.split()
        first_word = words[0]
        if first_word in LANG_CODE_LIST:
            lang_code = first_word
            to_translate = " ".join(words[1:])
    
    if not text and not to_translate and context_args: # /tr text | lang_code = database
        to_translate = context_args

    elif text and not to_translate: # /tr (maybe lang_code or maybe not) and replied
        to_translate = text
    
    if not lang_code:
        if chat.type == ChatType.PRIVATE:
            collection_name = "users"
            to_find = "user_id"
            to_match = user.id
        else:
            collection_name = "groups"
            to_find = "chat_id"
            to_match = chat.id

        database_data = database_search(collection_name, to_find, to_match)
        if not database_data:
            await effective_message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
            return
        
        lang_code = database_data.get("lang")
    
    if not lang_code:
        btn = ButtonMaker.ubutton([{"Language code's": "https://telegra.ph/Language-Code-12-24"}])
        await effective_message.reply_text("Chat language code wasn't found! Use /tr to get more details or /settings to set chat language.", reply_markup=btn)
        return
    
    sent_message = await effective_message.reply_text("💭 Translating...")

    translated_text = translate(to_translate, lang_code)
    if translated_text == False:
        btn = ButtonMaker.ubutton([{"Language code's": "https://telegra.ph/Language-Code-12-24"}])
        await context.bot.edit_message_text("Invalid language code was given! Use /tr to get more details or /settings to set chat language.", chat.id, sent_message.id, reply_markup=btn)

    elif not translated_text:
        await context.bot.edit_message_text("Oops! Something went wrong!", chat.id, sent_message.id)

    else:
        await context.bot.edit_message_text(translated_text, chat.id, sent_message.id)
