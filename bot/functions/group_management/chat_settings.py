import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from bot import logger
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.helper.messages_storage import chat_settings_menu_group
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_search
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins

async def chat_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function won't be in handler, instead it will be called in func_settings if chat.type isn't private"""
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
        return
    
    chat_admins = await fetch_chat_admins(chat, user_id=user.id)
    
    if not (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins["is_user_admin"] and not chat_admins["is_user_admin"].can_change_info:
        await effective_message.reply_text("You don't have enough permission to manage this chat!")
        return
    
    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "groups",
        "db_find": "chat_id",
        "db_vlaue": chat.id,
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": effective_message.id,
        "edit_data_value_msg_pointer_id": None
    }
    
    MemoryDB.insert_data("data_center", chat.id, data)

    response, database_data = database_search("groups", "chat_id", chat.id)
    if response == False:
        await effective_message.reply_text(database_data)
        return
    
    title = database_data.get("title")
    lang = database_data.get("lang")
    echo = database_data.get("echo", False)
    auto_tr = database_data.get("auto_tr", False)
    welcome_user = database_data.get("welcome_user", False)
    farewell_user = database_data.get("farewell_user", False)
    antibot = database_data.get("antibot", False)
    is_links_allowed = database_data.get("is_links_allowed")
    allowed_links_list = database_data.get("allowed_links_list")
    
    if allowed_links_list:
        allowed_links_list = ", ".join(allowed_links_list)

    text = chat_settings_menu_group.format(
        title,
        chat.id,
        lang,
        auto_tr,
        echo,
        antibot,
        welcome_user,
        farewell_user,
        is_links_allowed,
        allowed_links_list
    )

    btn_data = [
        {"Language": "query_chat_lang", "Auto translate": "query_chat_auto_tr"},
        {"Echo": "query_chat_set_echo", "Anti bot": "query_chat_antibot"},
        {"Welcome": "query_chat_welcome_user", "Farewell": "query_chat_farewell_user"},
        {"Links behave": "query_chat_links_behave", "Close": "query_close"}
    ]

    btn = ButtonMaker.cbutton(btn_data)

    images = MemoryDB.bot_data.get("images")
    photo = random.choice(images).strip() if images else MemoryDB.bot_data.get("bot_pic")

    if photo:
        try:
            await effective_message.reply_photo(photo, text, reply_markup=btn)
        except BadRequest:
            photo = None
        except Exception as e:
            logger.error(e)
    
    if not photo:
        await effective_message.reply_text(text, reply_markup=btn)
