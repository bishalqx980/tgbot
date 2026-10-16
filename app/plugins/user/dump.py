import asyncio
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


class DUMP_DATA:
    # collection name for database
    DUMP_COLLECTION_NAME = "dumps"
    DUMP_MESSAGE_1 = (
        "> Dump Information\n\n"
        "• Dumper ID : `{dumper_id}`\n"
        "• Title : {title}\n"
        "• Key : `{key}`\n"
        "• Self-destruct : {self_destruct}\n"
        "• Content Restriction : {content_restriction}\n"
        "• Link Restriction : {link_restriction}\n\n"

        "<i>Note:\n"
        "• Self-destruct will delete document automatically.\n"
        "• Content Restriction will lock the document. No one will be able to take screenshot or download it (viewonly)\n"
        "• Link Restriction will disable the link. No one will be able to get the document through link.</i>"
    )


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

        try:

            dump_files = await re_msg.get_media_group()
            message_ids = [msg.id for msg in dump_files]

        except ValueError:

            message_ids = [re_msg.id]
        
        key = uuid4().hex[:16]

        forwarded_message = await bot.forward_messages(
            chat_id=config.dump_channel,
            from_chat_id=message.chat.id,
            message_ids=message_ids,
            hide_sender_name=True,
            hide_captions=False
        )

        forwarded_message_id = forwarded_message[0].id
        forwarded_message_ids = [msg.id for msg in forwarded_message]

        if not title:
            title = re_msg.caption or key[:8]

        MongoDB.insert(
            DUMP_DATA.DUMP_COLLECTION_NAME,
            key,
            {
                "key": key,
                "title": title,
                "user_id": user.id, # file saver user id
                "message_ids": forwarded_message_ids
            }
        )

        bot_url = f"http://t.me/{bot.me.username}/?start=dump_{key}"
        btn = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Get the document", url=bot_url)
            ],
            [
                InlineKeyboardButton("Toggle Self-destruct", f"dump:self_destruct:{key}"),
                InlineKeyboardButton("Toggle Content Restriction", f"dump:content_restriction:{key}"),
                InlineKeyboardButton("Toggle Link Restriction", f"dump:link_restriction:{key}")
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
            (
                "Document has been saved successfully.\n\n" +
                DUMP_DATA.DUMP_MESSAGE_1.format(
                    dumper_id=user.id,
                    title=title,
                    key=key,
                    self_destruct="Disabled",
                    content_restriction="Disabled",
                    link_restriction="Disabled"
                )
            ),
            reply_markup=btn
        )

        # Save info on dump channel too
        await bot.send_message(
            config.dump_channel,
            DUMP_DATA.DUMP_MESSAGE_1.format(
                dumper_id=user.id,
                title=title,
                key=key,
                self_destruct="Disabled",
                content_restriction="Disabled",
                link_restriction="Disabled"
            ),
            reply_parameters=ReplyParameters(message_id=forwarded_message_id),
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

    # Toggle Self-destruct
    if query_data.startswith("self_destruct:"):
        key = query_data.removeprefix("self_destruct:")

        data = MongoDB.search(
            DUMP_DATA.DUMP_COLLECTION_NAME,
            "key",
            key
        )
    
        if not data:
            return await query.answer(
                "Error: Invalid key!",
                True
            )

        self_destruct = data.get("self_destruct")

        response = MongoDB.update(
            DUMP_DATA.DUMP_COLLECTION_NAME,
            "key",
            key,
            { "self_destruct": None if self_destruct else 30 }
        )

        if response:
            await query.answer(
                f"✅ {'Disabled' if self_destruct else 'Enabled'} Self-destruct timer!",
                True
            )
        
        else:
            return await query.answer(
                "❌ Failed to toggle Self-destruct timer!",
                True
            )

        try:

            data = MongoDB.search(
                DUMP_DATA.DUMP_COLLECTION_NAME,
                "key",
                key
            )

            dumper_id = data["user_id"]
            title = data["title"]
            self_destruct = data.get("self_destruct")
            content_restriction = data.get("content_restriction")
            link_restriction = data.get("link_restriction")

            await query.edit_message_text(
                DUMP_DATA.DUMP_MESSAGE_1.format(
                    dumper_id=dumper_id,
                    title=title,
                    key=key,
                    self_destruct=self_destruct or "Disabled",
                    content_restriction="Enabled" if content_restriction else "Disabled",
                    link_restriction="Enabled" if link_restriction else "Disabled"
                ),
                reply_markup=query.message.reply_markup
            )

        except:
            pass
    
    # Toggle Restrict Content
    elif query_data.startswith("content_restriction:"):
        key = query_data.removeprefix("content_restriction:")

        data = MongoDB.search(
            DUMP_DATA.DUMP_COLLECTION_NAME,
            "key",
            key
        )
    
        if not data:
            return await query.answer(
                "Error: Invalid key!",
                True
            )

        content_restriction = data.get("content_restriction")

        response = MongoDB.update(
            DUMP_DATA.DUMP_COLLECTION_NAME,
            "key",
            key,
            { "content_restriction": False if content_restriction else True }
        )

        if response:
            await query.answer(
                f"✅ {'Disabled' if content_restriction else 'Enabled'} Content Restriction!",
                True
            )
        
        else:
            return await query.answer(
                "❌ Failed to toggle Content Restriction!",
                True
            )

        try:

            data = MongoDB.search(
                DUMP_DATA.DUMP_COLLECTION_NAME,
                "key",
                key
            )

            dumper_id = data["user_id"]
            title = data["title"]
            self_destruct = data.get("self_destruct")
            content_restriction = data.get("content_restriction")
            link_restriction = data.get("link_restriction")

            await query.edit_message_text(
                DUMP_DATA.DUMP_MESSAGE_1.format(
                    dumper_id=dumper_id,
                    title=title,
                    key=key,
                    self_destruct=self_destruct or "Disabled",
                    content_restriction="Enabled" if content_restriction else "Disabled",
                    link_restriction="Enabled" if link_restriction else "Disabled"
                ),
                reply_markup=query.message.reply_markup
            )

        except:
            pass


    # Toggle Disable Link
    elif query_data.startswith("link_restriction:"):
        key = query_data.removeprefix("link_restriction:")

        data = MongoDB.search(
            DUMP_DATA.DUMP_COLLECTION_NAME,
            "key",
            key
        )
    
        if not data:
            return await query.answer(
                "Error: Invalid key!",
                True
            )

        link_restriction = data.get("link_restriction")

        response = MongoDB.update(
            DUMP_DATA.DUMP_COLLECTION_NAME,
            "key",
            key,
            { "link_restriction": False if link_restriction else True }
        )

        if response:
            await query.answer(
                f"✅ {'Disabled' if link_restriction else 'Enabled'} Link Restriction!",
                True
            )
        
        else:
            return await query.answer(
                "❌ Failed to toggle Link Restriction!",
                True
            )

        try:

            data = MongoDB.search(
                DUMP_DATA.DUMP_COLLECTION_NAME,
                "key",
                key
            )

            dumper_id = data["user_id"]
            title = data["title"]
            self_destruct = data.get("self_destruct")
            content_restriction = data.get("content_restriction")
            link_restriction = data.get("link_restriction")

            await query.edit_message_text(
                DUMP_DATA.DUMP_MESSAGE_1.format(
                    dumper_id=dumper_id,
                    title=title,
                    key=key,
                    self_destruct=self_destruct or "Disabled",
                    content_restriction="Enabled" if content_restriction else "Disabled",
                    link_restriction="Enabled" if link_restriction else "Disabled"
                ),
                reply_markup=query.message.reply_markup
            )

        except:
            pass
    
    # delete key from database
    elif query_data.startswith("delete:"):
        key = query_data.removeprefix("delete:")

        # Get the database info before deleting
        data = MongoDB.search(
            DUMP_DATA.DUMP_COLLECTION_NAME,
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
            DUMP_DATA.DUMP_COLLECTION_NAME,
            "key",
            key
        )

        if is_deleted:
            try:

                # +1 of the original message ID
                bot_message_id = data["message_ids"][-1] + 1

                await bot.edit_message_text(
                    chat_id=config.dump_channel,
                    message_id=bot_message_id,
                    text=(
                        "> Dump Information\n\n"
                        f"• Dumper ID : `{data['user_id']}`\n"
                        f"• Title : `{data['title']}`\n"
                        f"• Message ID : `{', '.join(map(str, data['message_ids']))}`\n\n"
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
                    message_ids=data["message_ids"],
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
        DUMP_DATA.DUMP_COLLECTION_NAME,
        "key",
        key
    )

    if not data:
        return await message.reply(
            "Error: Invalid key!"
        )
    
    dumper_id = data["user_id"]
    title = data["title"]
    message_ids = data["message_ids"]

    self_destruct = data.get("self_destruct")
    content_restriction = data.get("content_restriction")
    link_restriction = data.get("link_restriction")

    if link_restriction and message.from_user.id != dumper_id:
        return await message.reply(
            "⚠️ Private link!"
        )
    
    sent_message = await bot.forward_messages(
        chat_id=message.chat.id,
        from_chat_id=config.dump_channel,
        message_ids=message_ids,
        hide_sender_name=True,
        hide_captions=False,
        protect_content=content_restriction
    )

    sent_message = sent_message[0]

    if dumper_id == message.from_user.id:
        bot_url = f"http://t.me/{bot.me.username}/?start=dump_{key}"

        await sent_message.reply(
            DUMP_DATA.DUMP_MESSAGE_1.format(
                dumper_id=dumper_id,
                title=title,
                key=key,
                self_destruct=self_destruct or "Disabled",
                content_restriction="Enabled" if content_restriction else "Disabled",
                link_restriction="Enabled" if link_restriction else "Disabled"
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Get the document", url=bot_url)
                ],
                [
                    InlineKeyboardButton("Toggle Self-destruct", f"dump:self_destruct:{key}"),
                    InlineKeyboardButton("Toggle Content Restriction", f"dump:content_restriction:{key}"),
                    InlineKeyboardButton("Toggle Link Restriction", f"dump:link_restriction:{key}")
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
        )

    # self-destruct auto delete timer set
    if self_destruct:
        try:
            await asyncio.sleep(self_destruct)
            await sent_message.delete()
        except Exception as e:
            logger.error(e)
