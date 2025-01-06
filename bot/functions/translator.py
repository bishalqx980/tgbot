from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import global_search
from bot.modules.database.combined_db import find_bot_docs
from bot.modules.translator import LANG_CODE_LIST, translate


async def func_translator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    re_msg = update.message.reply_to_message
    msg = (re_msg.text_html or re_msg.caption_html) if re_msg else None
    input_text = " ".join(context.args)

    if not msg and not input_text:
        btn_data = {
            "Language code's": "https://telegra.ph/Language-Code-12-24"
        }
        btn = await Button.ubutton(btn_data)
        await Message.reply_message(update, "Use <code>/tr text</code> or <code>/tr lang_code text</code> or reply the text with <code>/tr</code> or <code>/tr lang_code</code>\n\nEnable auto translator mode for this chat from /settings", btn=btn)
        return
    
    to_translate = None
    lang_code = None
    
    if input_text:
        words = input_text.split()
        first_word = words[0]
        if first_word in LANG_CODE_LIST:
            lang_code = first_word
            to_translate = " ".join(words[1:])
    
    if not msg and not to_translate and input_text: # /tr text and lang_code = get from db
        to_translate = input_text
    
    if msg and not to_translate: # /tr (maybe lang_code or maybe not) and replied
        to_translate = msg
    
    if not lang_code:
        if chat.type == "private":
            collection_name = "users"
            to_find = "user_id"
            to_match = user.id
        else:
            collection_name = "groups"
            to_find = "chat_id"
            to_match = chat.id

        db = await global_search(collection_name, to_find, to_match)
        if db[0] == False:
            await Message.reply_message(update, db[1])
            return
        
        find_chat = db[1]
        
        lang_code = find_chat.get("lang")

    tr_msg = await translate(to_translate, lang_code)
    if tr_msg:
        sent_msg = await Message.reply_message(update, tr_msg)
        if not sent_msg:
            await Message.reply_message(update, "Oops, something went wrong...")
        return

    if not tr_msg:
        _bot = await find_bot_docs()
        if not _bot:
            return
        
        btn_data = {
            "Language code's": "https://telegra.ph/Language-Code-12-24"
        }
        btn = await Button.ubutton(btn_data)
        await Message.send_message(chat.id, "Chat language not found/invalid! Use /settings to set chat language.", btn=btn)
