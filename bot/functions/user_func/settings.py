from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.helper.button_maker import ButtonMaker
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_search
from ..group_management.chat_settings import chat_settings

class PvtChatSettingsData:
    TEXT = (
        "<blockquote><b>Chat Settings</b></blockquote>\n\n"

        "• Name: {}\n"
        "• ID: <code>{}</code>\n\n"

        "• Language: <code>{}</code>\n"
        "• Auto translate: <code>{}</code>\n"
        "• Echo: <code>{}</code>"
    )

    BUTTONS = [
        {"Language": "csettings_lang", "Auto translate": "csettings_auto_tr"},
        {"Echo": "csettings_echo", "Close": "csettings_close"}
    ]


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
    
    text = PvtChatSettingsData.TEXT.format(
        user.mention_html(),
        user.id,
        database_data.get('lang'),
        database_data.get('auto_tr') or False,
        database_data.get('echo') or False
    )

    btn = ButtonMaker.cbutton(PvtChatSettingsData.BUTTONS)
    
    await effective_message.reply_text(text, reply_markup=btn)
