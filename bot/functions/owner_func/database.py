import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.modules.database import MongoDB
from bot.helper.telegram_helpers.telegram_helper import Message
from bot.functions.power_users import _power_users


async def func_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    chat_id = " ".join(context.args)

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_message(update, "Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        await Message.reply_message(update, f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
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

        msg = (
            f"{msg_storage}" # already has 2 escapes
            f"<b>• Active users:</b> <code>{active_users}</code>\n"
            f"<b>• Inactive users:</b> <code>{inactive_users}</code>\n\n"
            f"<i>Note: <code>/database chat_id</code> to get specific chat database information.</i>"
        )

        await Message.reply_message(update, msg)
        return
    
    try:
        chat_id = int(chat_id)
    except ValueError:
        await Message.reply_message(update, "Invalid ChatID!")
        return

    # if chat_id given
    if "-100" in str(chat_id):
        find_group = MongoDB.find_one("groups", "chat_id", chat_id) # chat_id as int
        if not find_group:
            await Message.reply_message(update, "Chat not found!")
            return
        
        msg = (
            f"<b><u>Database info:</u> <code>{chat_id}</code></b>\n\n"
            f"<b>• Title:</b> <i>{find_group.get('title')}</i>\n"
            f"<b>• Lang:</b> <code>{find_group.get('lang', False)}</code>\n"
            f"<b>• Echo:</b> <code>{find_group.get('echo', False)}</code>\n"
            f"<b>• Auto tr:</b> <code>{find_group.get('auto_tr', False)}</code>\n"
            f"<b>• Welcome user:</b> <code>{find_group.get('welcome_user', False)}</code>\n"
            f"<b>• Farewell user:</b> <code>{find_group.get('farewell_user', False)}</code>\n"
            f"<b>• Anti bot:</b> <code>{find_group.get('antibot', False)}</code>\n"
            f"<b>• Delete cmd:</b> <code>{find_group.get('del_cmd', False)}</code>\n"
            f"<b>• All links:</b> <code>{find_group.get('all_links')}</code>\n"
            f"<b>• Allowed links:</b> <code>{find_group.get('allowed_links')}</code>\n"
            f"<b>• Log channel:</b> <code>{find_group.get('log_channel')}</code>\n"
            f"<b>• Chat filters:</b>\n"
            f"<blockquote>{find_group.get('filters')}</blockquote>\n"
            f"<b>• Custom welcome message:</b>\n"
            f"<blockquote>{find_group.get('custom_welcome_msg')}</blockquote>\n"
        )
    else:
        find_user = MongoDB.find_one("users", "user_id", chat_id) # chat_id as int
        if not find_user:
            await Message.reply_message(update, "User not found!")
            return
        
        msg = (
            f"<b><u>Database info:</u> <code>{chat_id}</code></b>\n\n"
            f"<b>• Name:</b> <i>{find_user.get('name')}</i>\n"
            f"<b>• Username:</b> @{find_user.get('username')}\n"
            f"<b>• Mention:</b> {find_user.get('mention')}\n"
            f"<b>• Lang:</b> <code>{find_user.get('lang')}</code>\n"
            f"<b>• Echo:</b> <code>{find_user.get('echo')}</code>\n"
            f"<b>• Active status:</b> <code>{find_user.get('active_status')}</code>\n"
        )
    
    # common message sender for both group chat & private chat database info
    await Message.reply_message(update, msg)
