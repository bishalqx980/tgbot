from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.utils.database import DBConstants, MemoryDB, database_search
from .auxiliary.chat_admins import ChatAdmins
from .auxiliary.anonymous_admin import anonymousAdmin


class GroupChatSettingsData:
    TEXT = (
        "<blockquote><b>Chat Settings</b></blockquote>\n\n"

        "• Title: {}\n"
        "• ID: <code>{}</code>\n\n"

        "• Language: <code>{}</code>\n"
        "• Auto translate: <code>{}</code>\n"
        "• Echo: <code>{}</code>\n"
        "• Antibot: <code>{}</code>\n"
        "• Welcome Members: <code>{}</code>\n"
        "• Farewell Members: <code>{}</code>\n"
        "• Join Request: <code>{}</code>\n"
        "• Service Messages: <code>{}</code>\n"
        "• Links Behave: <code>{}</code>\n"
        "• Allowed Links: <code>{}</code>"
    )

    BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Language", callback_data="csettings_lang"),
            InlineKeyboardButton("Auto translate", callback_data="csettings_auto_tr")
        ],
        [
            InlineKeyboardButton("Echo", callback_data="csettings_echo"),
            InlineKeyboardButton("Antibot", callback_data="csettings_antibot")
        ],
        [
            InlineKeyboardButton("Welcome Members", callback_data="csettings_welcome_user"),
            InlineKeyboardButton("Farewell Members", callback_data="csettings_farewell_user")
        ],
        [
            InlineKeyboardButton("Links Behave", callback_data="csettings_links_behave"),
            InlineKeyboardButton("Allowed Links", callback_data="csettings_allowed_links")
        ],
        [
            InlineKeyboardButton("Join Request",callback_data="csettings_chat_join_req"),
            InlineKeyboardButton("Service Messages", callback_data="csettings_service_messages")
        ],
        [
            InlineKeyboardButton("Close", callback_data="csettings_close")
        ]
    ])


async def chat_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function won't be in handler, instead it will be called in func_settings if chat.type isn't private"""
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    if user.is_bot:
        user = await anonymousAdmin(chat, effective_message)
        if not user:
            return
    
    chat_admins = ChatAdmins()
    await chat_admins.fetch_admins(chat, context.bot.id, user.id)
    
    if not (chat_admins.is_user_admin or chat_admins.is_user_owner):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins.is_user_admin and not chat_admins.is_user_admin.can_change_info:
        await effective_message.reply_text("You don't have enough permission to manage this chat!")
        return
    
    if not chat_admins.is_bot_admin:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    chat_data = database_search(DBConstants.CHATS_DATA, "chat_id", chat.id)
    if not chat_data:
        await effective_message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return
    
    data = {
        "user_id": user.id, # authorization
        "collection_name": DBConstants.CHATS_DATA,
        "search_key": "chat_id",
        "match_value": chat.id
    }
    
    MemoryDB.insert(DBConstants.DATA_CENTER, chat.id, data)
    
    await effective_message.reply_text(
        GroupChatSettingsData.TEXT.format(
            chat.title,
            chat.id,
            chat_data.get('lang') or '-',
            'Enabled' if chat_data.get('auto_tr') else 'Disabled',
            'Enabled' if chat_data.get('echo') else 'Disabled',
            'Enabled' if chat_data.get('antibot') else 'Disabled',
            'Enabled' if chat_data.get('welcome_user') else 'Disabled',
            'Enabled' if chat_data.get('farewell_user') else 'Disabled',
            chat_data.get('chat_join_req'),
            'Enabled' if chat_data.get('service_messages') else 'Disabled',
            chat_data.get('links_behave'), # this contains a value
            ', '.join(chat_data.get('allowed_links') or [])
        ),
        reply_markup=GroupChatSettingsData.BUTTONS
    )
