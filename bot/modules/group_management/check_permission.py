from telegram import Update
from bot import bot
from bot.helper.telegram_helper import Message

async def _check_permission(update: Update, victim=None, user=None, checking_msg=True):
    chat = update.effective_chat

    if checking_msg:
        del_msg = await Message.send_msg(chat.id, "Checking permission...")

    _bot_info = await bot.get_me()
    bot_permission = await chat.get_member(_bot_info.id)

    user_permission = await chat.get_member(user.id) if user else None
    victim_permission = await chat.get_member(victim.id) if victim else None
    
    if checking_msg:
        await Message.del_msg(chat.id, del_msg)

    return _bot_info, bot_permission, user_permission, victim_permission
