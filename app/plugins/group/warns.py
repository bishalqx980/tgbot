from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus

from app import bot, logger, COMMAND_PREFIXES
from app.decorators import groupchat_only
from app.helpers import CommandArgs
from app.database import MongoDB


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "warns",
    "commands": ["warns"], # list of commands including aliases

    "description": "Check your warning's in current chat!",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Warns", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
async def func_(_, message: Message):
    re_msg = message.reply_to_message
    args = CommandArgs(message.text, message.command)

    if not message.from_user:
        return await message.reply(
            "Huh, Ghost detected >.<"
        )

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
    
    if not victim:
        victim = message.from_user
    
    if victim.id == bot.me.id:
        return await message.reply_text(
            "I will leave this job soon -_-"
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

    victim_warns = warns.setdefault(str(victim.id), [])
    warn_count = len(victim_warns)

    if warn_count > 0:
        reasons = []

        for warn_info in victim_warns:
            reason = warn_info.get("reason")
            timestamp = warn_info.get("timestamp")
            admin = warn_info.get("admin")
            
            reasons.append(
                f"• {reason} - `{datetime.fromtimestamp(timestamp)}` - by {admin}"
            )

        reasons = '\n'.join(reasons)

        await message.reply_text(
            f"Warnings of {victim.mention}\n\n"
            f"Total warnings : `{warn_count}`\n"
            f"Reasons :\n{reasons}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "Remove All Warnings (admin only)",
                    callback_data=f"rem_allwarn:{victim.id}"
                )
            ]])
        )

    else:
        await message.reply(
            f"{victim.mention} doesn't have any warning."
        )


@bot.on_callback_query(filters.regex(r"^rem_allwarn:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):

    if query.data.startswith("rem_allwarn:"):
        victim_id = query.data.removeprefix("rem_allwarn:")

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
                victim_warns.clear()

                MongoDB.update(
                    MongoDB.CHATS,
                    "chat_id",
                    query.message.chat.id,
                    { "warns": warns }
                )

                await query.edit_message_text(
                    f"All Warning has been removed by {query.from_user.mention}!"
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
