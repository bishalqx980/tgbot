from functools import wraps

from pyrogram.types import Message, User, Chat
from pyrogram.enums import ChatMemberStatus

from app import bot, logger
from app.helpers import verify_anonymous_admin


def bot_admin(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            chat_bot_data = await message.chat.get_member(
                bot.me.id
            )

            if chat_bot_data.status != ChatMemberStatus.ADMINISTRATOR:
                return await message.reply_text(
                    "I'm not an admin in this chat!"
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def bot_can_restrict(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            chat_bot_data = await message.chat.get_member(
                bot.me.id
            )

            if not chat_bot_data.privileges.can_restrict_members:
                return await message.reply_text(
                    "I don't have enough permission to restrict chat members!\n"
                    "Make sure that I'm an admin in this chat and has permission to restrict chat members."
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def bot_can_promote(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            chat_bot_data = await message.chat.get_member(
                bot.me.id
            )

            if not chat_bot_data.privileges.can_promote_members:
                return await message.reply_text(
                    "I don't have enough permission to promote/demote chat members!\n"
                    "Make sure that I'm an admin in this chat and has permission to promote/demote chat members."
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def bot_can_invite(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            chat_bot_data = await message.chat.get_member(
                bot.me.id
            )

            if not chat_bot_data.privileges.can_invite_users:
                return await message.reply_text(
                    "I don't have enough permission to invite members in this chat!\n"
                    "Make sure that I'm an admin in this chat and has permission to invite members in this chat."
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def bot_can_manage_chat(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            chat_bot_data = await message.chat.get_member(
                bot.me.id
            )

            if not chat_bot_data.privileges.can_manage_chat:
                return await message.reply_text(
                    "I don't have enough permission to manage this chat!\n"
                    "Make sure that I'm an admin in this chat and has permission to manage this chat."
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def bot_can_pin_messages(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            chat_bot_data = await message.chat.get_member(
                bot.me.id
            )

            if not chat_bot_data.privileges.can_pin_messages:
                return await message.reply_text(
                    "I don't have enough permission to pin/unpin messages in this chat!\n"
                    "Make sure that I'm an admin in this chat and has permission to pin/unpin messages in this chat."
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def bot_can_delete_messages(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            chat_bot_data = await message.chat.get_member(
                bot.me.id
            )

            if not chat_bot_data.privileges.can_delete_messages:
                return await message.reply_text(
                    "I don't have enough permission to delete messages in this chat!\n"
                    "Make sure that I'm an admin in this chat and has permission to delete messages in this chat."
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def user_admin(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            user = message.from_user or message.sender_chat

            # anonymous admin verification
            if isinstance(user, Chat):
                user = await verify_anonymous_admin(message)
                if not isinstance(user, User):
                    return

            chat_user_data = await message.chat.get_member(
                user.id
            )

            if chat_user_data.status not in [
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER
            ]:
                return await message.reply_text(
                    "You aren't an admin in this chat!"
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def user_can_restrict(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            user = message.from_user or message.sender_chat

            # anonymous admin verification
            if isinstance(user, Chat):
                user = await verify_anonymous_admin(message)
                if not isinstance(user, User):
                    return

            chat_user_data = await message.chat.get_member(
                user.id
            )

            if not chat_user_data.privileges.can_restrict_members:
                return await message.reply_text(
                    "You don't have enough permission to restrict chat members!"
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def user_can_promote(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            user = message.from_user or message.sender_chat

            # anonymous admin verification
            if isinstance(user, Chat):
                user = await verify_anonymous_admin(message)
                if not isinstance(user, User):
                    return

            chat_user_data = await message.chat.get_member(
                user.id
            )

            if not chat_user_data.privileges.can_promote_members:
                return await message.reply_text(
                    "You don't have enough permission to promote/demote chat members!"
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def user_can_invite(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            user = message.from_user or message.sender_chat

            # anonymous admin verification
            if isinstance(user, Chat):
                user = await verify_anonymous_admin(message)
                if not isinstance(user, User):
                    return

            chat_user_data = await message.chat.get_member(
                user.id
            )

            if not chat_user_data.privileges.can_invite_users:
                return await message.reply_text(
                    "You don't have enough permission to invite members in this chat!"
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def user_can_manage_chat(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            user = message.from_user or message.sender_chat

            # anonymous admin verification
            if isinstance(user, Chat):
                user = await verify_anonymous_admin(message)
                if not isinstance(user, User):
                    return

            chat_user_data = await message.chat.get_member(
                user.id
            )

            if not chat_user_data.privileges.can_manage_chat:
                return await message.reply_text(
                    "You don't have enough permission to manage this chat!"
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def user_can_pin_messages(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            user = message.from_user or message.sender_chat

            # anonymous admin verification
            if isinstance(user, Chat):
                user = await verify_anonymous_admin(message)
                if not isinstance(user, User):
                    return

            chat_user_data = await message.chat.get_member(
                user.id
            )

            if not chat_user_data.privileges.can_pin_messages:
                return await message.reply_text(
                    "You don't have enough permission to pin/unpin messages in this chat!"
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper


def user_can_delete_messages(func):
    @wraps(func)
    async def wraper(_, message: Message):
        try:

            user = message.from_user or message.sender_chat

            # anonymous admin verification
            if isinstance(user, Chat):
                user = await verify_anonymous_admin(message)
                if not isinstance(user, User):
                    return

            chat_user_data = await message.chat.get_member(
                user.id
            )

            if not chat_user_data.privileges.can_delete_messages:
                return await message.reply_text(
                    "You don't have enough permission to delete messages in this chat!"
                )
            
        except Exception as e:
            logger.error(e)
            return await message.reply_text(f"Error: {e}")
        
        return await func(_, message)
    return wraper
