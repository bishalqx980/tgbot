from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from ...helper.button_maker import ButtonMaker
from ...modules.database import MemoryDB
from ...modules.database.common import database_search
from ..group_management.chat_settings import chat_settings

async def func_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    if chat.type != ChatType.PRIVATE:
        await chat_settings(update, context)
        return
    
    data = {
        "user_id": user.id, # authorization
        "collection_name": "users",
        "search_key": "user_id",
        "match_value": user.id
    }

    MemoryDB.insert("data_center", user.id, data)

    database_data = database_search("users", "user_id", user.id)
    if not database_data:
        await effective_message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return
    
    text = (
        "<blockquote><b>Chat Settings</b></blockquote>\n\n"

        f"• Name: {user.mention_html()}\n"
        f"• ID: <code>{user.id}</code>\n\n"

        f"• Language: <code>{database_data.get('lang')}</code>\n"
        f"• Auto translate: <code>{database_data.get('auto_tr') or False}</code>\n"
        f"• Echo: <code>{database_data.get('echo') or False}</code>"
    )

    btn_data = [
        {"Language": "csettings_lang", "Auto translate": "csettings_auto_tr"},
        {"Echo": "csettings_echo", "Close": "csettings_close"}
    ]

    btn = ButtonMaker.cbutton(btn_data)
    await effective_message.reply_text(text, reply_markup=btn)
