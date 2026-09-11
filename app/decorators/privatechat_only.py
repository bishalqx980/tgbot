import asyncio
from functools import wraps

from pyrogram.types import Message
from pyrogram.enums import ChatType

from app import bot, logger


def privatechat_only(func):
    @wraps(func)
    async def wraper(_, message: Message):
        chat = message.chat

        if chat.type != ChatType.PRIVATE:
            sent_message = await message.reply(
                "This command is made to be used in private chat, not in group chats!"
            )

            await asyncio.sleep(3)

            try:
                await bot.delete_messages(
                    chat.id,
                    [
                        message.id,
                        sent_message.id
                    ]
                )
            except Exception as e:
                logger.error(e)
            
            return
        return await func(_, message)
    return wraper
