from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.button_maker import ButtonMaker
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_search
from .auxiliary.fetch_chat_admins import fetch_chat_admins

async def chat_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function won't be in handler, instead it will be called in func_settings if chat.type isn't private"""
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message

    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
        return
    
    chat_admins = await fetch_chat_admins(chat, context.bot.id, user.id)
    
    if not (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins["is_user_admin"] and not chat_admins["is_user_admin"].can_change_info:
        await effective_message.reply_text("You don't have enough permission to manage this chat!")
        return
    
    if not chat_admins["is_bot_admin"]:
        await effective_message.reply_text("I'm not an admin in this chat!")
        return
    
    database_data = database_search("groups", "chat_id", chat.id)
    if not database_data:
        await effective_message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return
    
    data = {
        "user_id": user.id, # authorization
        "collection_name": "groups",
        "search_key": "chat_id",
        "match_value": chat.id
    }
    
    MemoryDB.insert("data_center", chat.id, data)

    text = (
        "<blockquote><b>Chat Settings</b></blockquote>\n\n"

        f"• Title: {chat.title}\n"
        f"• ID: <code>{chat.id}</code>\n\n"

        f"• Language: <code>{database_data.get('lang')}</code>\n"
        f"• Auto translate: <code>{database_data.get('auto_tr') or False}</code>\n"
        f"• Echo: <code>{database_data.get('echo') or False}</code>\n"
        f"• Antibot: <code>{database_data.get('antibot') or False}</code>\n"
        f"• Welcome Members: <code>{database_data.get('welcome_user') or False}</code>\n"
        f"• Farewell Members: <code>{database_data.get('farewell_user') or False}</code>\n"
        f"• Join Request: <code>{database_data.get('chat_join_req')}</code>\n"
        f"• Service Messages: <code>{database_data.get('service_messages')}</code>\n"
        f"• Links Behave: <code>{database_data.get('links_behave')}</code>\n"
        f"• Allowed Links: <code>{', '.join(database_data.get('allowed_links') or [])}</code>"
    )

    btn_data = [
        {"Language": "csettings_lang", "Auto translate": "csettings_auto_tr"},
        {"Echo": "csettings_echo", "Antibot": "csettings_antibot"},
        {"Welcome Members": "csettings_welcome_user", "Farewell Members": "csettings_farewell_user"},
        {"Links Behave": "csettings_links_behave", "Allowed Links": "csettings_allowed_links"},
        {"Join Request": "csettings_chat_join_req", "Service Messages": "csettings_service_messages"},
        {"Close": "csettings_close"}
    ]

    btn = ButtonMaker.cbutton(btn_data)
    await effective_message.reply_text(text, reply_markup=btn)
