from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import Forbidden
from bot import owner_id
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.modules.database.combined_db import find_bot_docs, check_add_user_db


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not owner_id:
        msg = f"owner_id: <code>{chat.id}</code>\nPlease add owner_id in <code>config.env</code> file then retry. Otherwise bot won't work properly." if chat.type == "private" else "Error <i>owner_id</i> not provided!"
        await Message.reply_message(update, msg)
        return
    
    _bot_info = await LOCAL_DATABASE.find("_bot_info")

    if chat.type != "private":
        sent_msg = await Message.send_message(user.id, ".")
        if sent_msg == Forbidden:
            await Message.reply_message(update, f"Hey, {user.mention_html()}!\n<a href='{_bot_info.get('link')}'>Start me</a> in pm to chat with me!")
            return
        elif sent_msg:
            await Message.reply_message(update, f"<a href='{_bot_info.get('link')}'>Sent in your pm!</a>")
            await Message.delete_message(user.id, sent_msg)
    
    _bot = await find_bot_docs()
    if not _bot:
        return
    
    bot_pic = _bot.get("bot_pic")
    welcome_img = _bot.get("welcome_img")
    support_chat = _bot.get("support_chat")

    msg = (
        f"Hey, {user.first_name}! I'm {_bot_info.get('first_name')}!\n"
        "I can help you to manage your group with lots of useful features!\n"
        "Feel free to add me to your group.\n\n"
        "<b>/help - for bot help</b>\n\n"
        "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
        "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
        "<b>• Developer:</b> <a href='https://t.me/bishalqx980'>bishalqx980</a>"
    )

    if _bot_info.get("username") != "MissCiri_bot":
        msg += "\n\n<i>Cloned bot of @MissCiri_bot</i>"

    btn_data_1 = {
        "Add me to your Group": f"{_bot_info.get('link')}?startgroup=start"
    }

    btn_data_2 = {
        "Support Chat": support_chat
    }

    row_1 = await Button.ubutton(btn_data_1)
    btn = row_1

    if support_chat:
        row_2 = await Button.ubutton(btn_data_2)
        btn = row_1 + row_2
    
    sent_img = await Message.send_image(user.id, bot_pic, msg, btn=btn) if welcome_img and bot_pic else None
    if not sent_img:
        await Message.send_message(user.id, msg, btn=btn)
    
    await check_add_user_db(user)
