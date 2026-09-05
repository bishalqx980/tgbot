from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ChatType

from bot.utils.database import DBConstants, MemoryDB, database_search
from ..group.chat_settings import chat_settings


class PvtChatSettingsData:
    TEXT = (
        "<blockquote><b>Chat Settings</b></blockquote>\n\n"

        "• Name: {}\n"
        "• ID: <code>{}</code>\n\n"

        "• Language: <code>{}</code>\n"
        "• Auto translate: <code>{}</code>\n"
        "• Echo: <code>{}</code>"
    )

    BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Language", callback_data="csettings_lang"),
            InlineKeyboardButton("Auto translate", callback_data="csettings_auto_tr")
        ],
        [
            InlineKeyboardButton("Echo", callback_data="csettings_echo"),
            InlineKeyboardButton("Close", callback_data="misc_close")
        ]
    ])


async def func_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    if chat.type not in [ChatType.PRIVATE]:
        await chat_settings(update, context)
        return
    
    data = {
        "user_id": user.id, # authorization
        "collection_name": DBConstants.USERS_DATA,
        "search_key": "user_id",
        "match_value": user.id
    }

    MemoryDB.insert(DBConstants.DATA_CENTER, user.id, data)

    user_data = database_search(DBConstants.USERS_DATA, "user_id", user.id)
    if not user_data:
        return await effective_message.reply_text(
            "<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>"
        )
    
    await effective_message.reply_text(
        PvtChatSettingsData.TEXT.format(
            user.mention_html(),
            user.id,
            user_data.get('lang') or '-',
            'Enabled' if user_data.get('auto_tr') else 'Disabled',
            'Enabled' if user_data.get('echo') else 'Disabled'
        ),
        reply_markup=PvtChatSettingsData.BUTTONS
    )
