import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helpers.telegram_helper import Message
from bot.functions.power_users import _power_users

async def func_get_invitelink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    chat_id = " ".join(context.args)

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_message(update, "Access denied!")
        return
    
    if chat.type != "private":
        await Message.reply_message(update, f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    if not chat_id:
        await Message.reply_message(update, "<code>/invitelink chat_id</code> to get specified chat invite link.\n<i>Note: only works if this bot is in that chat and have enough permissions to get invite link!</i>")
        return
    
    sent_msg = await Message.reply_message(update, "Please wait...")

    try:
        expire_date = datetime.now() + timedelta(days=1)
        invite_link = await bot.create_chat_invite_link(chat_id, expire_date=expire_date, member_limit=1)
    except Exception as e:
        await Message.edit_message(update, str(e), sent_msg)
        return
    
    await Message.edit_message(update, f"<b>Generated link:</b> {invite_link.invite_link}", sent_msg)
