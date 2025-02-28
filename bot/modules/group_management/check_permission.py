from telegram import Update
from bot import bot

async def _check_permission(update: Update, victim=None, user=None):
    """
    returns `dict` of >> `bot_permission`, `user_permission`, `victim_permission`\n
    returns `bot_permission` as default
    """
    chat = update.effective_chat

    bot_permission = await chat.get_member(bot.id)
    user_permission = await chat.get_member(user.id) if user else None
    victim_permission = await chat.get_member(victim.id) if victim else None

    data = {
        "bot_permission": bot_permission,
        "user_permission": user_permission,
        "victim_permission": victim_permission
    }
    
    return data
