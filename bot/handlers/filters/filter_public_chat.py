from telegram import Update, ChatMember
from telegram.ext import ContextTypes

from bot import TL_LANG_CODES_URL
from bot.helpers import BuildKeyboard
from bot.utils.database import DBConstants, database_search
from .edit_database import edit_database
from .auto_linkblocker import autoLinkBlocker
from .auto_translate import autoTranslate
from .auto_triggers import autoTriggers

async def filter_public_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    message = update.message

    is_editing = edit_database(chat.id, user.id, message)
    if is_editing:
        return
    
    chat_data = database_search(DBConstants.CHATS_DATA, "chat_id", chat.id)
    if not chat_data:
        await message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return
    
    # Auto Link Blocker
    links_behave = chat_data.get("links_behave") # 3 values: delete; convert; None;
    filtered_text = None

    if links_behave:
        # check if user is admin or owner
        member_info = await chat.get_member(user.id)
        if member_info.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
            link_rules = {"links_behave": links_behave, "allowed_links": chat_data.get("allowed_links")}
            is_forbidden = await autoLinkBlocker(message, user, link_rules)

            if is_forbidden:
                filtered_text = is_forbidden
    
    # Echo message
    if chat_data.get("echo") and not filtered_text:
        await message.reply_text(message.text_html or message.caption_html)

    # Auto Translator
    auto_tr = chat_data.get("auto_tr")
    chat_lang = chat_data.get("lang")

    if auto_tr and not chat_lang:
        btn = BuildKeyboard.ubutton([{"Language code's": TL_LANG_CODES_URL}])
        await message.reply_text("Chat language code wasn't found! Use /settings to set chat language.", reply_markup=btn)
    
    elif auto_tr and not filtered_text:
        await autoTranslate(message, user, chat_lang)
    
    # Auto Trigers
    filters = chat_data.get("filters")
    if filters:
        await autoTriggers(message, user, chat, filters)
