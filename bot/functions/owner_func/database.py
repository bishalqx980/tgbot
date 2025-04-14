import json
import asyncio
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from ...modules.database import MongoDB
from ...helper.button_maker import ButtonMaker
from ..sudo_users import fetch_sudos

async def func_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    victim_id = " ".join(context.args)

    sudo_users = fetch_sudos()
    if user.id not in sudo_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await context.bot.delete_messages(chat.id, [effective_message.id, sent_message.id])
        return
    
    if not victim_id:
        database_info = MongoDB.info()
        msg_storage = "<b><u>Database</u></b>\n\n"
        for info in database_info:
            info = database_info[info]
            msg_storage += (
                f"<b>• Document:</b> <i>{info.get('name')}</i>\n"
                f"<b>• Quantity:</b> <code>{info.get('quantity')}</code>\n"
                f"<b>• Size:</b> <code>{info.get('size')}</code>\n"
                f"<b>• A. size:</b> <code>{info.get('acsize')}</code>\n\n"
            )
        
        active_status = MongoDB.find("users", "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        text = (
            f"{msg_storage}" # already has 2 escapes
            f"<b>• Active users:</b> <code>{active_users}</code>\n"
            f"<b>• Inactive users:</b> <code>{inactive_users}</code>\n\n"
            f"<blockquote><b>Note:</b> <code>/database ChatID</code> to get specific chat database information.</blockquote>"
        )

        await effective_message.reply_text(text)
        return
    
    try:
        victim_id = int(victim_id)
    except ValueError:
        await effective_message.reply_text("Invalid ChatID!")
        return

    # if chat_id given
    if "-100" in str(victim_id):
        database_data = MongoDB.find_one("groups", "chat_id", victim_id) # victim_id as int
        if not database_data:
            await effective_message.reply_text("Chat not found!")
            return
        
        try:
            victim_info = await context.bot.get_chat(victim_id)
        except:
            victim_info = None
            btn = None
        
        chat_title = victim_info.title if victim_info else database_data.get('title')
        chat_invite_link = victim_info.invite_link if victim_info else None

        text = (
            "<blockquote><b>Database information</b></blockquote>\n\n"

            f"• Title: {chat_title}\n"
            f"• ID: <code>{victim_id}</code>\n\n"

            f"• Language: <code>{database_data.get('lang')}</code>\n"
            f"• Auto translate: <code>{database_data.get('auto_tr') or False}</code>\n"
            f"• Echo: <code>{database_data.get('echo') or False}</code>\n"
            f"• Antibot: <code>{database_data.get('antibot') or False}</code>\n"
            f"• Welcome Members: <code>{database_data.get('welcome_user') or False}</code>\n"
            f"• Farewell Members: <code>{database_data.get('farewell_user') or False}</code>\n"
            f"• Join Request: <code>{database_data.get('chat_join_req')}</code>\n"
            f"• Links Behave: <code>{database_data.get('links_behave')}</code>\n"
            f"• Allowed Links: <code>{', '.join(database_data.get('allowed_links') or [])}</code>"
        )

        btn = ButtonMaker.ubutton([{"Invite Link": chat_invite_link}]) if chat_invite_link else None
        
        custom_welcome_msg = database_data.get('custom_welcome_msg')
        if custom_welcome_msg:
            text += (
                "\n\n<blockquote><b>Custom Welcome message</b></blockquote>\n\n"
                f"<blockquote>{custom_welcome_msg}</blockquote>"
            )
        
        chat_filters = database_data.get('filters')
        if chat_filters:
            filters_file = BytesIO(json.dumps(chat_filters, indent=4).encode())
            filters_file.name = f"filters_{victim_id}.json"

            await effective_message.reply_document(filters_file, f"ChatID: <code>{victim_id}</code>")
    
    else:
        database_data = MongoDB.find_one("users", "user_id", victim_id) # victim_id as int
        if not database_data:
            await effective_message.reply_text("User not found!")
            return
        
        try:
            victim_info = await context.bot.get_chat(victim_id)
        except:
            victim_info = None
            btn = None
        
        victim_name = victim_info.mention_html() if victim_info else database_data.get('mention')
        victim_username = victim_info.username if victim_info else database_data.get('username')
        text = "<blockquote><b>Database information</b></blockquote>\n\n"

        text += (
            f"• Name: {victim_name}\n"
            f"• ID: <code>{victim_id}</code>\n"
            f"• Username: @{victim_username or 'username'}\n\n"

            f"• Language: <code>{database_data.get('lang')}</code>\n"
            f"• Auto translate: <code>{database_data.get('auto_tr') or False}</code>\n"
            f"• Echo: <code>{database_data.get('echo') or False}</code>\n\n"

            f"• Active status: <code>{database_data.get('active_status')}</code>"
        )

        if victim_info:
            btn = ButtonMaker.ubutton([{"User Profile": f"tg://user?id={victim_info.id}"}]) if victim_info.username else None
    
    # common message sender for both group chat & private chat database info
    await effective_message.reply_text(text, reply_markup=btn)
