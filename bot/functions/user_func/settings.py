import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest
from bot import logger
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_search
from bot.functions.group_management.chat_settings import chat_settings

async def func_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    if chat.type != ChatType.PRIVATE:
        await chat_settings(update, context)
        return
    
    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "users",
        "search_key": "user_id",
        "match_value": user.id,
        "update_data_key": None,
        "update_data_value": None,
        "edit_value_message_id": None,
        "effective_message_id": effective_message.id
    }

    MemoryDB.insert("data_center", chat.id, data)

    response, database_data = database_search("users", "user_id", user.id)
    if response == False:
        await effective_message.reply_text(database_data)
        return
    
    user_mention = database_data.get("mention")
    lang = database_data.get("lang")
    echo = database_data.get("echo", False)
    auto_tr = database_data.get("auto_tr", False)

    text = (
        "<u><b>Chat Settings</b></u>\n\n"
        f"• User: {user_mention}\n"
        f"• ID: <code>{chat.id}</code>\n\n"

        f"• Lang: <code>{lang}</code>\n"
        f"• Echo: <code>{echo}</code>\n"
        f"• Auto tr: <code>{auto_tr}</code>\n\n"
    )

    btn_data = [
        {"Language": "query_chat_lang", "Auto translate": "query_chat_auto_tr"},
        {"Echo": "query_chat_set_echo", "Close": "query_close"}
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
