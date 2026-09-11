from functools import wraps

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType

from app import bot


def groupchat_only(func):
    @wraps(func)
    async def wraper(_, message: Message):
        if message.chat.type == ChatType.PRIVATE:
            return await message.reply(
                "This command is made to be used in group chats, not in private chat!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                    "Add Me",
                    url=f"https://{bot.me.username}.t.me?startgroup=help"
                )]])
            )
        
        return await func(_, message)
    return wraper
