from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import Forbidden
from bot import bot, owner_id
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import find_bot_docs, check_add_user_db


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not owner_id:
        msg = f"owner_id: <code>{chat.id}</code>\nPlease add owner_id in <code>config.env</code> file then retry. Otherwise bot won't work properly." if chat.type == "private" else "Error <i>owner_id</i> not provided!"
        await Message.reply_msg(update, msg)
        return
    
    _bot_info = await bot.get_me()

    if chat.type != "private":
        sent_msg = await Message.send_msg(user.id, ".")
        if sent_msg == Forbidden:
            await Message.reply_msg(update, f"Hey, {user.mention_html()}!\n<a href='http://t.me/{_bot_info.username}'>Start me</a> in pm to chat with me!")
            return
        elif sent_msg:
            await Message.reply_msg(update, f"<a href='http://t.me/{_bot_info.username}'>Sent in your pm!</a>")
            await Message.del_msg(user.id, sent_msg)
    
    _bot = await find_bot_docs()
    if not _bot:
        return
    
    bot_pic = _bot.get("bot_pic")
    welcome_img = _bot.get("welcome_img")
    support_chat = _bot.get("support_chat")

    msg = (
        f"Hey, {user.first_name}! I'm {_bot_info.first_name}!\n"
        "I can help you to manage your group with lots of useful features!\n"
        "Feel free to add me to your group.\n\n"
        "<b>/help - for bot help</b>\n\n"
        "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
        "<b>• Developer:</b> <a href='https://t.me/bishalqx980'>bishalqx980</a>"
    )

    if _bot_info.username != "MissCiri_bot":
        msg += "\n\n<i>Cloned bot of @MissCiri_bot</i>"

    btn_name_1 = ["Add me to your Group"]
    btn_url_1 = [f"http://t.me/{_bot_info.username}?startgroup=start"]
    btn_name_2 = ["Support Chat"]
    btn_url_2 = [support_chat]

    row_1 = await Button.ubutton(btn_name_1, btn_url_1)
    btn = row_1

    if support_chat:
        row_2 = await Button.ubutton(btn_name_2, btn_url_2)
        btn = row_1 + row_2
    
    if welcome_img and bot_pic:
        await Message.send_img(user.id, bot_pic, msg, btn)
    else:
        await Message.send_msg(user.id, msg, btn)
    
    await check_add_user_db(user)
