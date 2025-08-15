from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus

from bot.utils.decorators.pm_error import pm_error
from bot.helpers import BuildKeyboard
from .auxiliary.anonymous_admin import anonymousAdmin

@pm_error
async def func_leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    
    if user.is_bot:
        user = await anonymousAdmin(chat, effective_message)
        if not user:
            return
    
    try:
        user_status = await chat.get_member(user.id)
    except Exception as e:
        await effective_message.reply_text(str(e))
        return

    if user_status.status not in [ChatMemberStatus.OWNER]:
        await effective_message.reply_text("Huh, you aren't the owner of this chat!")
        return
    
    btn = BuildKeyboard.cbutton([{"Leave": "misc_leavechat", "Stay": "misc_close"}])
    await effective_message.reply_text("Should I leave?", reply_markup=btn)
