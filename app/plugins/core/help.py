import random
from math import ceil

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
from pyrogram.errors import BadRequest

from app import bot, logger, config, MODULES, HELP_MENU_CATEGORIES, ADMIN_CATEGORIES, COMMAND_PREFIXES
from app.database import MongoDB, SessionData


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "help",
    "commands": ["help"], # list of commands including aliases

    "description": "Get Help!",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


def GenerateHelpMenu(category = None, page = 1):
    # Dynamically generates button list from Modules
    plugins = []
    BTN_PER_PAGE = 9
    BTN_PER_ROW = 3
    
    for plugin in MODULES.values():
        if category is not None and plugin["category"] != category:
            continue

        if not plugin["button_name"]:
            continue

        plugins.append(plugin)
    
    # Pages logic
    total_pages = max(1, ceil(len(plugins) / BTN_PER_PAGE))
    page = max(1, min(page, total_pages))

    start = (page - 1) * BTN_PER_PAGE
    end = start + BTN_PER_PAGE

    current_plugins = plugins[start:end]

    message = f"> **Help Menu <i>({category})</i>**\n\n"
    buttons = []
    row = []

    for plugin in current_plugins:
        message += f"- /{plugin['commands'][0]} : <i>{plugin['description']}</i>\n"

        row.append(
            InlineKeyboardButton(plugin["button_name"], f"help:{plugin['category']}:{plugin['_id']}")
        )

        if len(row) == BTN_PER_ROW:
            buttons.append(row)
            row = []

    # Remaining buttons
    if row:
        buttons.append(row)

    # Navigation buttons
    nav = []
    back_btn = InlineKeyboardButton(f"◀ Back ({page - 1})", f"help_nav:{category}:{page - 1}")
    next_btn = InlineKeyboardButton(f"▶ Next ({page + 1})", f"help_nav:{category}:{page + 1}")

    if page > 1:
        nav.append(back_btn)
        
    if page < total_pages:
        nav.append(next_btn)
    
    buttons.append(nav)

    # Main Menu buttons
    buttons.append([
        InlineKeyboardButton("☰ Menu", "help:menu"),
        InlineKeyboardButton("✘ Close", "help:close")
    ])

    return {
        "message": message,
        "button": InlineKeyboardMarkup(buttons)
    }


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES) | filters.regex(r"^/start help$"))
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
                InlineKeyboardButton("Get help in PM", url=f"https://{bot.me.username}.t.me?start=help")
            ]])
        )

    bot_data = MongoDB.get_bot_data()
    bool_botpic = bot_data.get("bool_botpic")
    bot_images = bot_data.get("bot_images")
    photo = None
    photo_file_id = None

    text = (
        "> **Help Menu**\n\n"

        "• /start : Bot intro!\n"
        "• /help : Get Help! (this message)\n"
        "• /support : Get Support! OR report anything related to this bot."
    )

    row = []
    btn = []

    for category in HELP_MENU_CATEGORIES:

        row.append(
            InlineKeyboardButton(category.title(), f"help:{category}:")
        )

        if len(row) == 3:
            btn.append(row)
            row = []

    # Remaining row buttons
    btn.append(row)

    # other buttons
    btn.append([
        InlineKeyboardButton("✘ Close", "help:close"),
        InlineKeyboardButton("Try inline", switch_inline_query_current_chat="")
    ])

    btn = InlineKeyboardMarkup(btn)

    # Store data for callback menu
    SessionData.insert(data={
        "help_message": text,
        "help_buttons": btn
    })

    if bot_images:
        photo = random.choice(bot_images).strip()
    elif bool_botpic:
        try:
            async for photo in bot.get_chat_photos("me", 1):
                photo_file_id = photo.file_id
        except:
            pass
    
    try:
        if photo or photo_file_id:
            try:
                return await message.reply_photo(
                    photo or photo_file_id,
                    text,
                    reply_markup=btn
                )
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
        if not user_registered:
            user_info = {
                "user_id": user.id,
                "dc_id": user.dc_id,
                "name": user.full_name,
                "username": user.username,
                "usernames": user.usernames,
                "lang": user.language_code,
                "active_status": True
            }

            MongoDB.insert(MongoDB.USERS, user.id, user_info)


# Callback for Help Menu Navigation
@bot.on_callback_query(filters.regex(r"^help_nav:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    # case: callback_data = f"help_nav:category:page_number"
    query_data = query.data.removeprefix("help_nav:")
    category, page_number = query_data.split(":")

    await query.answer()

    menu_data = GenerateHelpMenu(category, int(page_number))

    text = menu_data["message"]
    btn = menu_data["button"]

    try:
        await query.edit_message_caption(text, reply_markup=btn)
    except BadRequest:
        await query.edit_message_text(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)


# Callback for Help Menu
@bot.on_callback_query(filters.regex(r"^help:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    # case1: callback_data = f"help:category:"
    # case2: callback_data = f"help:category:{__module__['_id']}"

    query_data = query.data.removeprefix("help:")
    category = None

    # case1
    if ":" in query_data:
        category, plugin_id = query_data.split(":")

    if category and not plugin_id:

        # Admin Verification for admin section
        if category in ADMIN_CATEGORIES:
            bot_data = MongoDB.get_bot_data()
            sudo_users = bot_data.get("sudo_users") or []
            
            if config.owner_id not in sudo_users:
                sudo_users.append(config.owner_id)
            
            if query.from_user.id not in sudo_users:
                await query.answer("Access denied!", True)
                return
        
        # Verified:
        await query.answer()

        menu_data = GenerateHelpMenu(category)

        text = menu_data["message"]
        btn = menu_data["button"]
    
    elif query_data == "menu":
        text = SessionData.get("help_message")
        btn = SessionData.get("help_buttons")

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
    
    # case2
    elif plugin_id:
        # query_data is plugin "_id"
        module_data = MODULES.get(plugin_id)

        if not module_data:
            return await query.answer("Invalid query data!", True)
        
        text = (
            f"**Name :** `{module_data['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in module_data['commands'])}\n"
            f"**Description :** <i>{module_data['description']}</i>\n\n"

            f"**Version :** `{module_data['version']}`\n"
            f"**Author :** `{module_data['author']}`\n\n"

            f"#{module_data['_id']}"
        )
        
        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton("◀ Back", f"help:{category}:"),
            InlineKeyboardButton("✘ Close", "help:close"),
            InlineKeyboardButton("☰ Menu", "help:menu")
        ]])

    else:
        return await query.answer("World of madness!!", True)
    
    # global reply
    try:
        await query.edit_message_caption(text, reply_markup=btn)
    except BadRequest:
        await query.edit_message_text(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)
