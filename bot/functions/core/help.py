import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import bot
from bot.helper.telegram_helpers.telegram_helper import Message, Button
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_add_user


async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if chat.type != ChatType.PRIVATE:
        btn = await Button.ubutton([{"Click here for help": f"{bot.link}?start=help"}])
        await Message.reply_message(update, f"Hey, {user.first_name}\nContact me in PM for help!", btn=btn)
        return
    
    msg = (
        f"Hey, {user.full_name}! Welcome to the bot help section.\n"
        "I'm a Telegram bot that manages groups and handles various tasks effortlessly.\n\n"
        "/start - to start the bot\n"
        "/help - to see this message\n\n"
        "<b>Note:</b> <i>The bot is compatible with the <code>/</code>, <code>!</code>, <code>.</code> and <code>-</code> command prefixes.</i>"
    )

    btn_data = [
        {"Group Management": "query_help_group_management_p1", "AI": "query_help_ai"},
        {"misc": "query_help_misc_functions", "Bot owner": "query_help_owner_functions"},
        {"» bot.info()": "query_help_bot_info", "Close": "query_close"}
    ]

    btn = await Button.cbutton(btn_data)

    images = MemoryDB.bot_data.get("images")
    if images:
        image = random.choice(images).strip()
    else:
        image = MemoryDB.bot_data.get("bot_pic")

    sent_img = await Message.reply_image(update, image, msg, btn=btn) if image else None
    if not sent_img:
        await Message.reply_message(update, msg, btn=btn)
    
    database_add_user(user)
