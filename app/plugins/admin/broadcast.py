import asyncio

from pyrogram import filters
from pyrogram.types import Message

from app import bot, logger, COMMAND_PREFIXES
from app.decorators import admin_require, privatechat_only
from app.database import MongoDB
from app.modules.utils import UTILITY


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "broadcast",
    "commands": ["broadcast", "bcast"], # list of commands including aliases

    "description": "Broadcast message to bot users!",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Broadcast", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@admin_require
async def func_(_, message: Message):
    re_msg = message.reply_to_message

    if not re_msg:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )

    PHOTO = re_msg.photo.file_id if re_msg.photo else None
    TEXT = re_msg.text or re_msg.caption

    sent_message = await message.reply(
        "Please wait..."
    )

    user_ids = MongoDB.get_field_values(MongoDB.USERS, "user_id")

    sent = 0
    failed = []

    for uid in user_ids:

        try:

            if PHOTO:
                res = await bot.send_photo(
                    uid,
                    PHOTO,
                    TEXT
                )

            else:
                res = await bot.send_message(
                    uid,
                    TEXT
                )

            if res:
                user_registered = MongoDB.search(MongoDB.USERS, "user_id", uid)
                
                if user_registered:
                    active_status = user_registered.get("active_status")
                    
                    if not active_status:
                        MongoDB.update(
                            MongoDB.USERS,
                            "user_id",
                            uid,
                            { "active_status": True }
                        )

                sent += 1

        except Exception as e:
            logger.error(e)
            failed.append(f"{uid} : {e}")

        await asyncio.sleep(0.5)

    

    try:

        percent = (sent + len(failed)) * 100 / len(user_ids)
        progress_bar = UTILITY.createProgressBar(percent)

        await sent_message.edit_text(
            "> **Broadcast**\n\n"

            "**📦 Database information**\n"
            f"**• Total users:** `{len(user_ids)}`\n"
            "**• Active users:** N/A\n\n"

            "**📊 Progress**\n"
            f"**• Sent:** `{sent}`\n"
            f"**• Exception:** `{len(failed)}`\n"
            f"**• Progress:** `{percent}%`\n"
            f"{progress_bar}" # progress bar
        )

    except Exception as e:
        await message.reply(str(e))
