from time import time
from uuid import uuid4

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus

from app import bot, logger, COMMAND_PREFIXES
from app.decorators import (
    groupchat_only,
    bot_admin,
    user_admin
)
from app.helpers import CommandArgs
from app.database import MongoDB


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "warn",
    "commands": ["warn", "dwarn"], # list of commands including aliases

    "description": "Give warning to a chat member! E.g. `/warn @username reason` or reply a member with `/warn reason`!",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Warn", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
@user_admin
@bot_admin
async def func_(_, message: Message):
    re_msg = message.reply_to_message
    args = CommandArgs(message.text, message.command)

    # priority: @username > reply
    if "@" in args:
        username, _, reason = args.partition(" ")

        # Extra useless work ?
        try:

            info = await message.chat.get_member(username)
            victim = info.user

        except Exception as e:
            return await message.reply_text(
                f"Error: {e}"
            )

    else:
        victim = re_msg.from_user if re_msg else None
        reason = args
    
    command = message.command[0]

    try:

        if command.startswith("d"):
            await bot.delete_messages(
                message.chat.id,
                [
                    message.id,
                    re_msg.id
                ]
            )
        
    except:
        pass
    
    if not victim:
        return await message.reply_text(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    if victim.id == bot.me.id:
        return await message.reply_text(
            "Hahaha, Nice try kiddo."
        )

    chat_data = MongoDB.search(
        MongoDB.CHATS,
        "chat_id",
        message.chat.id
    )

    if not chat_data:
        return await message.reply(
            "Error: Please use /reload to fix."
        )

    warns = chat_data.get("warns", {})

    # Convert existing user ID keys to strings
    warns = {
        str(victim_id): victim_warns
        for victim_id, victim_warns in warns.items()
    }

    remwarn_key = uuid4().hex

    warns.setdefault(str(victim.id), []).append({
        "user_id": victim.id,
        "reason": reason or "",
        "timestamp": int(time()),
        "admin": message.from_user.mention if message.from_user else "Anonymous",
        "remove_key": remwarn_key
    })

    MongoDB.update(
        MongoDB.CHATS,
        "chat_id",
        message.chat.id,
        { "warns": warns }
    )

    await message.reply_text(
        f"{victim.mention} has been warned!\n"
        f"Reason : <i>{reason}</i>\n\n"
        "• /warns - to check your warnings...",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Remove warn (admin only)",
                callback_data=f"remwarn:{victim.id}:{remwarn_key}"
            )
        ]])
    )


@bot.on_callback_query(filters.regex(r"^remwarn:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):

    if query.data.startswith("remwarn:"):
        victim_id, remwarn_key = query.data.removeprefix("remwarn:").split(":")

        try:

            user = query.from_user

            chat_user_data = await query.message.chat.get_member(
                user.id
            )

            if chat_user_data.status not in [
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER
            ]:
                return await query.answer(
                    "You aren't an admin in this chat!",
                    True
                )

            chat_data = MongoDB.search(
                MongoDB.CHATS,
                "chat_id",
                query.message.chat.id
            )

            if not chat_data:
                return await query.message.reply(
                    "Error: Please use /reload to fix."
                )
            
            warns = chat_data.get("warns", {})

            victim_warns = warns.setdefault(str(victim_id), [])
            warn_count = len(victim_warns)

            if warn_count > 0:
                for warn_info in victim_warns:
                    remove_key = warn_info.get("remove_key")

                    if remove_key == remwarn_key:
                        victim_warns.remove(warn_info)
                        break
                
                MongoDB.update(
                    MongoDB.CHATS,
                    "chat_id",
                    query.message.chat.id,
                    { "warns": warns }
                )

                await query.edit_message_text(
                    f"Warning has been removed by {query.from_user.mention}!"
                )

            else:
                return await query.answer(
                    "User doesn't have any warnings."
                )
            
        except Exception as e:
            logger.error(e)
            return await query.message.reply(
                f"Error: {e}"
            )
