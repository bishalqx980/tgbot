from uuid import uuid4

from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.decorators import privatechat_only, sudo_required
from app.utils.logger import LOG_PATH


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "log",
    "commands": ["log"], # list of commands including aliases

    "description": "Get app.log file (to debug app)!",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Log", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@sudo_required
async def func_(_, message: Message):
    filename = f"log-{uuid4().hex}.log"

    await message.reply_document(
        document=open(LOG_PATH, "rb"),
        caption=filename,
        file_name=filename
    )
