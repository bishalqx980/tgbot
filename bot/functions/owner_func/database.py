import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.modules.database import MongoDB
from bot.functions.sudo_users import fetch_sudos

async def func_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    chat_id = " ".join(context.args)

    sudo_users = fetch_sudos()
    if user.id not in sudo_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await context.bot.delete_messages(chat.id, [effective_message.id, sent_message.id])
        return
    
    if not chat_id:
        database_info = MongoDB.info_db()
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
            f"<i>Note: <code>/database chat_id</code> to get specific chat database information.</i>"
        )

        await effective_message.reply_text(text)
        return
    
    try:
        chat_id = int(chat_id)
    except ValueError:
        await effective_message.reply_text("Invalid ChatID!")
        return

    # if chat_id given
    if "-100" in str(chat_id):
        database_data = MongoDB.find_one("groups", "chat_id", chat_id) # chat_id as int
        if not database_data:
            await effective_message.reply_text("Chat not found!")
            return
        
        text = (
            f"<b><u>Database info:</u> <code>{chat_id}</code></b>\n\n"
            f"<b>• Title:</b> <i>{database_data.get('title')}</i>\n"
            f"<b>• Lang:</b> <code>{database_data.get('lang', False)}</code>\n"
            f"<b>• Echo:</b> <code>{database_data.get('echo', False)}</code>\n"
            f"<b>• Auto tr:</b> <code>{database_data.get('auto_tr', False)}</code>\n"
            f"<b>• Welcome user:</b> <code>{database_data.get('welcome_user', False)}</code>\n"
            f"<b>• Farewell user:</b> <code>{database_data.get('farewell_user', False)}</code>\n"
            f"<b>• Anti bot:</b> <code>{database_data.get('antibot', False)}</code>\n"
            f"<b>• Delete cmd:</b> <code>{database_data.get('del_cmd', False)}</code>\n"
            f"<b>• All links:</b> <code>{database_data.get('all_links')}</code>\n"
            f"<b>• Allowed links:</b> <code>{database_data.get('allowed_links')}</code>\n"
            f"<b>• Log channel:</b> <code>{database_data.get('log_channel')}</code>\n"
            f"<b>• Chat filters:</b>\n"
            f"<blockquote>{database_data.get('filters')}</blockquote>\n"
            f"<b>• Custom welcome message:</b>\n"
            f"<blockquote>{database_data.get('custom_welcome_msg')}</blockquote>\n"
        )
    else:
        database_data = MongoDB.find_one("users", "user_id", chat_id) # chat_id as int
        if not database_data:
            await effective_message.reply_text("User not found!")
            return
        
        text = (
            f"<b><u>Database info:</u> <code>{chat_id}</code></b>\n\n"
            f"<b>• Name:</b> <i>{database_data.get('name')}</i>\n"
            f"<b>• Username:</b> @{database_data.get('username')}\n"
            f"<b>• Mention:</b> {database_data.get('mention')}\n"
            f"<b>• Lang:</b> <code>{database_data.get('lang')}</code>\n"
            f"<b>• Echo:</b> <code>{database_data.get('echo')}</code>\n"
            f"<b>• Active status:</b> <code>{database_data.get('active_status')}</code>\n"
        )
    
    # common message sender for both group chat & private chat database info
    await effective_message.reply_text(text)
