import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType


from bot.functions.sudo_users import _power_users

async def func_get_invitelink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    chat_id = " ".join(context.args)

    power_users = fetch_sudos()
    if user.id not in power_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    if not chat_id:
        await effective_message.reply_text("<code>/invitelink chat_id</code> to get specified chat invite link.\n<i>Note: only works if this bot is in that chat and have enough permissions to get invite link!</i>")
        return
    
    sent_msg = await effective_message.reply_text("Please wait...")

    try:
        expire_date = datetime.now() + timedelta(days=1)
        invite_link = await bot.create_chat_invite_link(chat_id, expire_date=expire_date, member_limit=1)
    except Exception as e:
        await Message.edit_message(update, str(e), sent_msg)
        return
    
    await Message.edit_message(update, f"<b>Generated link:</b> {invite_link.invite_link}", sent_msg)
