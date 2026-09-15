from pyrogram import filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from app import bot, COMMAND_PREFIXES
from app.database import MongoDB


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "whisper",
    "commands": ["whisper"], # list of commands including aliases

    "description": (
        "Whisper someone secretly in a public group! Only they can read the message.\n"
        "Usage: `@{bot_username} @username This is a Secret Message!`"
    ),
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Whisper", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}

# collection name for database
WHISPER_COLLECTION_NAME = "whispers"


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    return await message.reply(
        f"**Name :** `{__module__['name']}`\n"
        f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
        f"**Description :** <i>{__module__['description'].format(bot_username=bot.me.username)}</i>\n\n"

        f"**Version :** `{__module__['version']}`\n"
        f"**Author :** `{__module__['author']}`\n\n"

        f"#{__module__['_id']}"
    )


@bot.on_callback_query(filters.regex(r"^whisper:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    whisper_key = query.data.removeprefix("whisper:")

    whisper_data = MongoDB.search(
        WHISPER_COLLECTION_NAME,
        "key",
        whisper_key
    )

    if not whisper_data:
        return await query.edit_message_text(
            "Error: Invalid key.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Send another whisper!", switch_inline_query_current_chat="Demo Secret Message!")
            ]])
        )

    sender_id = whisper_data.get("sender_id")
    receiver_username = whisper_data.get("receiver_username") # without @
    message = whisper_data.get("message")

    if (
        query.from_user.id == sender_id
        or query.from_user.username == receiver_username
    ):
        try:

            await query.answer(
                message,
                True
            )

            # delete the whisper data from database if the receiver get it
            if query.from_user.username == receiver_username:
                MongoDB.delete(
                    WHISPER_COLLECTION_NAME,
                    "key",
                    whisper_key
                )

                await query.edit_message_text(
                    f"<i>@{receiver_username} read the whispered message.</i>",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Send another whisper!", switch_inline_query_current_chat="@username This is a Secret Message!")
                    ]])
                )

        except Exception as e:
            await query.answer(
                str(e),
                True
            )

    # Access Denied
    else:
        await query.answer(
            "⚠️ This whisper message isn't for you!",
            True
        )
