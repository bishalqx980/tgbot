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
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "botdump",
    "commands": ["save", "dump"], # list of commands including aliases

    "description": (
        "Store files/documents and generate a unique URL for later retrieval.\n"
        "E.g. Reply any document with this command to generate a unique URL. OR `/dump title`"
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
    title = CommandArgs(message.text, message.command)

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
                "title": title,
                "user_id": user.id, # file saver user id
                "message_id": forwarded_message.id
            }
        )

        bot_url = f"http://t.me/{bot.me.username}/?start=dump_{key}"
        btn = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Get the document", url=bot_url)
            ],
            [
                InlineKeyboardButton("Copy link", copy_text=bot_url),
                InlineKeyboardButton(
                    "Delete document",
                    f"dump:delete:{key}",
                    style=ButtonStyle.DANGER
                )
            ]
        ])

        await message.reply(
            "Document has been saved successfully.",
            reply_markup=btn
        )

        # Save info on dump channel too
        await bot.send_message(
            config.dump_channel,
            "> Dump Information\n\n"
            f"• Dumper ID : `{user.id}`\n"
            f"• Title : {title}\n"
            f"• Message Link : [{forwarded_message.id}]({forwarded_message.link})\n"
            f"• Key : `{key}`",
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

        # Get the database info before deleting
        data = MongoDB.search(
            DUMP_COLLECTION_NAME,
            "key",
            key
        )

        if not data:
            return await query.answer(
                "Error: Unable to fetch data from database!\nPossibly invalid key!"
            )

        # (Note: Need to add sudo_users access)
        sudo_users = [config.owner_id]

        if query.from_user.id != data["user_id"] and query.from_user.id not in sudo_users:
            return await query.answer(
                "Access denied!"
            )
        
        is_deleted = MongoDB.delete(
            DUMP_COLLECTION_NAME,
            "key",
            key
        )

        if is_deleted:
            try:

                # +1 of the original message ID
                bot_message_id = data["message_id"] + 1

                await bot.edit_message_text(
                    chat_id=config.dump_channel,
                    message_id=bot_message_id,
                    text=(
                        "> Dump Information\n\n"
                        f"• Dumper ID : `{data['user_id']}`\n"
                        f"• Title : `{data['title']}`\n"
                        f"• Message ID : `{data['message_id']}`\n\n"
                        "<i>Document has been deleted by dumper.</i>"
                    )
                )

            except Exception as e:
                logger.error(e)

            # responding dumper
            if query.from_user.id == data["user_id"]:
                await query.edit_message_text(
                    "Document has been deleted successfully."
                )

        else:
            return await query.answer(
                "Error: failed to delete the document."
            )

        # Send a alert message to the dumper if the document get deleted by sudo_users
        if query.from_user.id in sudo_users and query.from_user.id != data["user_id"]:
            try:

                # giving the document back to the dumper
                await bot.forward_messages(
                    chat_id=data["user_id"],
                    from_chat_id=config.dump_channel,
                    message_ids=data["message_id"],
                    hide_sender_name=True,
                    hide_captions=False
                )

                await bot.send_message(
                    data["user_id"],
                    f"Your dumped document has been deleted by {query.from_user.mention}!\n\n"
                    f"<i>Note: you can dump the document again using /{__module__['commands'][0]} command!</i>"
                )

            except Exception as e:
                logger.error(e)


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
    
    sent_message = await bot.forward_messages(
        chat_id=message.chat.id,
        from_chat_id=config.dump_channel,
        message_ids=data["message_id"],
        hide_sender_name=True,
        hide_captions=False
    )

    if data["user_id"] == message.from_user.id:
        bot_url = f"http://t.me/{bot.me.username}/?start=dump_{key}"

        await sent_message.reply(
            "Available option's.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Copy link", copy_text=bot_url),
                InlineKeyboardButton(
                    "Delete document",
                    f"dump:delete:{key}",
                    style=ButtonStyle.DANGER
                )
            ]])
        )
