from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, COMMAND_PREFIXES
from app.database import MongoDB
from app.decorators import privatechat_only


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "mydumps",
    "commands": ["mydumps", "dumps"], # list of commands including aliases

    "description": "Get your dump list so far through the bot.",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "My Dumps", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}

# collection name for database
DUMP_COLLECTION_NAME = "dumps"


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat

    sent_message = await message.reply(
        "Please wait..."
    )

    keys = MongoDB.get_field_values(
        DUMP_COLLECTION_NAME,
        "key"
    )

    # this will store str data for each dump
    lines = []
    buttons = []

    for key in keys:
        data = MongoDB.search(
            DUMP_COLLECTION_NAME,
            "key",
            key
        )

        # This will never gonna happen but im using the condition
        if not data:
            continue

        # skiping other users data
        if data["user_id"] != user.id:
            continue

        title = data.get("title")
        message_id = data.get("message_id")

        bot_url = f"http://t.me/{bot.me.username}/?start=dump_{key}"

        lines.append(
            f"• {title or '???'} : [Get the file]({bot_url})"
        )

        buttons.append(
            InlineKeyboardButton(title or message_id, url=bot_url)
        )

    if lines:
        text = '\n'.join(lines)
    else:
        text = "• You don't have any dumps yet."

    # 2 buttons on each row
    if buttons:
        rows = []

        for i in range(0, len(buttons), 2):
            row = buttons[i:i + 2]
            rows.append(row)

        buttons = InlineKeyboardMarkup(rows)
    
    await sent_message.edit(
        "> My Dump's\n\n"
        f"{text}",
        reply_markup=buttons
    )
