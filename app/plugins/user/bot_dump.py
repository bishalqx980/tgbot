from uuid import uuid4

from pyrogram import filters
from pyrogram.types import (
    Message,
    User,
    ReplyParameters,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.enums import ButtonStyle

from app import bot, logger, config, COMMAND_PREFIXES
from app.database import MongoDB


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "botdump",
    "commands": ["save", "dump"], # list of commands including aliases

    "description": (
        "Store files/documents and generate a unique URL for later retrieval.\n\n"
        "E.g. Reply any document with this command to generate a unique URL."
    ),
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Dump", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}

# collection name for database
DUMP_COLLECTION_NAME = "dumps"


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message

    if not isinstance(user, User):
        return await message.reply(
            "This feature is unavailable for anonymous users."
        )
    
    if not re_msg:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    try:

        key = uuid4().hex

        forwarded_message = await bot.forward_messages(
            chat_id=config.dump_channel,
            from_chat_id=message.chat.id,
            message_ids=re_msg.id,
            hide_sender_name=True,
            hide_captions=False
        )

        MongoDB.insert(
            DUMP_COLLECTION_NAME,
            key,
            {
                "key": key,
                "user_id": user.id, # file saver user id
                "message_id": forwarded_message.id
            }
        )

        bot_url = f"http://t.me/{bot.me.username}/?start=dump_{key}"
        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton("Copy Link", copy_text=bot_url),
            InlineKeyboardButton(
                "Delete file",
                f"dump:delete:{key}",
                style=ButtonStyle.DANGER
            )
        ]])

        await message.reply(
            "Document has been saved successfully.\n"
            f"• [Get the file]({bot_url})",
            reply_markup=btn
        )

        # Save info on dump channel too
        await bot.send_message(
            config.dump_channel,
            "> Dump Information\n\n"
            f"• Sender ID : `{user.id}`\n"
            f"• Message ID : `{forwarded_message.id}`\n"
            f"• Key : `{key}`\n"
            f"• [Get the file]({bot_url})",
            reply_parameters=ReplyParameters(message_id=forwarded_message.id),
            reply_markup=btn
        )

    except Exception as e:
        logger.error(e)
        return await message.reply(
            f"Error: {e}"
        )


@bot.on_callback_query(filters.regex(r"^dump:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    query_data = query.data.removeprefix("dump:")

    if query_data.startswith("delete:"):
        key = query_data.removeprefix("delete:")

        MongoDB.delete(
            DUMP_COLLECTION_NAME,
            "key",
            key
        )

        await query.edit_message_text(
            "File has been deleted successfully."
        )


@bot.on_message(filters.regex(r"^/start dump_(?P<key>[A-Za-z0-9_-]+)$"))
async def func_(_, message: Message):
    key = message.matches[0]["key"]

    data = MongoDB.search(
        DUMP_COLLECTION_NAME,
        "key",
        key
    )

    if not data:
        return await message.reply(
            "Error: Invalid key!"
        )
    
    await bot.forward_messages(
        chat_id=message.chat.id,
        from_chat_id=config.dump_channel,
        message_ids=data["message_id"],
        hide_sender_name=True,
        hide_captions=False
    )
