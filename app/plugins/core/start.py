from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
from pyrogram.errors import BadRequest

from app import bot, logger, __version__, __versionStatus__, COMMAND_PREFIXES, ORIGINAL_BOT_ID, ORIGINAL_BOT_USERNAME
from app.database import MongoDB, SessionData
from app.helpers import system_uptime


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "start",
    "commands": ["start"], # list of commands including aliases

    "description": "Bot Intro!",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES) & ~filters.regex("help"))
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    chat = message.chat

    if chat.type != ChatType.PRIVATE:
        # database entry checking if chat is registered.
        chat_registered = MongoDB.search(MongoDB.CHATS, "chat_id", chat.id)
        if not chat_registered:
            MongoDB.insert(MongoDB.CHATS, chat.id, { "chat_id": chat.id, "title": chat.title })
        
        return await message.reply(
            f"Hey, {user.first_name}\nWhy don't we start chatting in PM!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Start chatting in PM", url=f"https://{bot.me.username}.t.me?start=start")
            ]])
        )
    
    bot_data = MongoDB.get_bot_data()
    bool_botpic = bot_data.get("bool_botpic")
    link_supportchat = bot_data.get("link_supportchat")
    photo_file_id = None

    if bool_botpic:
        try:
            async for photo in bot.get_chat_photos("me", 1):
                photo_file_id = photo.file_id
        except:
            pass
    
    text = (
        f"Hey, {user.first_name}! I'm {bot.me.first_name}!\n\n"

        "I can help you to manage your **Group** with a lot of useful features!\n"
        "Feel free to add me to your **Group**.\n\n"

        "• /help - Get bot help menu\n\n"

        "**• Source code:** <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
        "**• Report bug:** <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
        "**• Developer:** <a href='https://t.me/bishalqx680/22'>bishalqx980</a>"
    )

    if bot.me.id != ORIGINAL_BOT_ID:
        text += f"\n\n> Cloned bot of @{ORIGINAL_BOT_USERNAME}"
    
    row_1 = [
        InlineKeyboardButton("Add Me", url=f"https://{bot.me.username}.t.me?startgroup=start"),
        InlineKeyboardButton("Get Help", url=f"https://{bot.me.username}.t.me?start=help")
    ]

    if link_supportchat:
        row_1.append(InlineKeyboardButton("Support Chat", url=link_supportchat))
    
    btn = InlineKeyboardMarkup([
        row_1,
        [
            InlineKeyboardButton("ღ About", "start:about")
        ]
    ])

    # Store data for callback menu
    SessionData.insert(data={
        "start_message": text,
        "start_buttons": btn
    })
    
    try:
        if photo_file_id:
            try:
                return await message.reply_photo(photo_file_id, text, reply_markup=btn)
            except BadRequest:
                pass
            except Exception as e:
                logger.error(e)
    
        # if BadRequest or No Photo or Other error
        await message.reply(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)
    
    finally:
        # database entry checking if user is registered.
        user_registered = MongoDB.search(MongoDB.USERS, "user_id", user.id)

        if user_registered:
            active_status = user_registered.get("active_status")
            
            if not active_status:
                MongoDB.update(
                    MongoDB.USERS,
                    "user_id",
                    user.id,
                    { "active_status": True }
                )

        else:
            MongoDB.insert(
                MongoDB.USERS,
                user.id,
                {
                    "user_id": user.id,
                    "dc_id": user.dc_id,
                    "name": user.full_name,
                    "username": user.username,
                    "usernames": user.usernames,
                    "lang": user.language_code,
                    "active_status": True
                }
            )


# Callback for Start Menu
@bot.on_callback_query(filters.regex(r"^start:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    query_data = query.data.removeprefix("start:")

    if query_data == "menu":
        text = SessionData.get("start_message")
        btn = SessionData.get("start_buttons")

        if not text or not btn:
            try:
                await query.message.delete()
            except:
                pass
            return
    
    elif query_data == "close":
            try:
                await query.answer()
            except:
                pass
    
            try:
                message_id = query.message.id
                await bot.delete_messages(query.message.chat.id, [message_id, message_id - 1])
            except:
                try:
                    await query.delete_message()
                except:
                    pass
            return
    
    elif query_data == "about":
        await query.answer("Getting information...")
        # Getting system & bot uptime
        uptime = system_uptime()

        text = (
            f"> **ღ About : {bot.me.first_name}**\n\n"

            f"**• Name :** {bot.me.mention}\n"
            f"**• ID :** `{bot.me.id}`\n"
            f"**• Username :** @{bot.me.username}\n\n"

            "**• Registered users :** `{t_users_count}`\n"
            "**• Active users :** `{active_users}`\n"
            "**• Inactive users :** `{inactive_users}`\n"
            "**• Total chats :** `{t_chats_count}`\n\n"

            f"**• System uptime :** `{uptime['system_uptime']}`\n"
            f"**• Bot uptime :** `{uptime['bot_uptime']}`\n"
            f"**• Version ({__versionStatus__}) :** `{__version__}`\n\n"

            "**<i>• /sysinfo : To get system info...</i>**"
        )

        # text without db info
        text_without_dbinfo = text.format(
            t_users_count = "loading...",
            active_users = "loading...",
            inactive_users = "loading...",
            t_chats_count = "loading..."
        )

        btn = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Source code", url = "https://github.com/bishalqx980/tgbot"),
                InlineKeyboardButton("Report bug", url = "https://github.com/bishalqx980/tgbot/issues")
            ],
            [
                InlineKeyboardButton("Developer", url = "https://t.me/bishalqx680/22"),
                InlineKeyboardButton("Buy me a Coffee", url = "https://telegra.ph/Buy-me-a-Coffee-03-01")
            ],
            [
                InlineKeyboardButton("◀ Back", "start:menu"),
                InlineKeyboardButton("✘ Close", "start:close")
            ]
        ])

        # sending response without db info (more efficient?)
        try:
            await query.edit_message_caption(text_without_dbinfo, reply_markup=btn)
        except BadRequest:
            await query.edit_message_text(text_without_dbinfo, reply_markup=btn)
        except Exception as e:
            logger.error(e)
        
        # loading database info
        database_info = MongoDB.database_info()

        i_users_data = database_info.get(MongoDB.USERS)
        i_chats_data = database_info.get(MongoDB.CHATS)

        t_users_count = i_users_data.get("quantity") if i_users_data else "Unknown"
        t_chats_count = i_chats_data.get("quantity") if i_chats_data else "Unknown"

        active_status = MongoDB.get_field_values(MongoDB.USERS, "active_status")
        active_users = active_status.count(True)
        inactive_users = active_status.count(False)

        # final formatting with db info
        text = text.format(
            t_users_count = t_users_count,
            active_users = active_users,
            inactive_users = inactive_users,
            t_chats_count = t_chats_count
        )
    
    # global reply
    try:
        await query.edit_message_caption(text, reply_markup=btn)
    except BadRequest:
        await query.edit_message_text(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)
