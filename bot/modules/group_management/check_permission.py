from telegram import Update
from bot.modules.database.local_database import LOCAL_DATABASE

async def _check_permission(update: Update, victim=None, user=None):
    """
    return's `dict` of >> `_bot_info`, `bot_permission`, `user_permission`, `victim_permission`
    """
    chat = update.effective_chat

    _bot_info = await LOCAL_DATABASE.find("_bot_info")
    bot_permission = await chat.get_member(_bot_info.get("id"))

    user_permission = await chat.get_member(user.id) if user else None
    victim_permission = await chat.get_member(victim.id) if victim else None

    data = {
        "_bot_info": _bot_info,
        "bot_permission": bot_permission,
        "user_permission": user_permission,
        "victim_permission": victim_permission
    }
    
    return data
