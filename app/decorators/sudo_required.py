from functools import wraps

from pyrogram.types import Message

from app import config
from app.database import MongoDB


def sudo_required(func):
    @wraps(func)
    async def wraper(_, message: Message):
        user = message.from_user or message.sender_chat
        owner_id = config.owner_id

        bot_data = MongoDB.get_bot_data()
        sudo_users = bot_data.get("sudo_users") or []

        if owner_id not in sudo_users:
            sudo_users.append(owner_id)
        
        if user.id not in sudo_users:
            return await message.reply("Access denied!")
        
        return await func(_, message)
    return wraper
