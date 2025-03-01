import random
from telegram import Update
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import find_bot_docs, check_add_user_db
from bot.modules.database.local_database import LOCAL_DATABASE


async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message

    if chat.type != "private":
        btn = await Button.ubutton({"Click here for help": f"{bot.link}?start=help"})
        await Message.reply_message(update, f"Hey, {user.first_name}\nContact me in PM for help!", btn=btn)
        return

    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "users",
        "db_find": "user_id",
        "db_vlaue": user.id,
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": e_msg.id,
        "edit_data_value_msg_pointer_id": None
    }

    await LOCAL_DATABASE.insert_data("data_center", user.id, data)

    msg = (
        f"Hey, {user.full_name}! Welcome to the bot help section.\n"
        "I'm a Telegram bot that manages groups and handles various tasks effortlessly.\n\n"
        "/start - to start the bot\n"
        "/help - to see this message\n\n"
        "<b>Note:</b> <i>The bot is compatible with the <code>/</code>, <code>!</code>, <code>.</code> and <code>-</code> command prefixes.</i>"
    )

    btn_data_row1 = {
        "Group Management": "query_help_group_management_p1",
        "AI": "query_help_ai"
    }

    btn_data_row2 = {
        "misc": "query_help_misc_functions",
        "Bot owner": "query_help_owner_functions"
    }

    btn_data_row3 = {
        "» bot.info()": "query_help_bot_info",
        "Close": "query_close"
    }

    row1 = await Button.cbutton(btn_data_row1, True)
    row2 = await Button.cbutton(btn_data_row2, True)
    row3 = await Button.cbutton(btn_data_row3, True)

    btn = row1 + row2 + row3

    _bot = await find_bot_docs()
    if not _bot:
        return
    
    images = _bot.get("images")
    if images:
        image = random.choice(images).strip()
    else:
        image = _bot.get("bot_pic")

    sent_img = await Message.send_image(user.id, image, msg, btn=btn) if image else None
    if not sent_img:
        await Message.send_message(user.id, msg, btn=btn)
    
    await check_add_user_db(user)
