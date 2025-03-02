from telegram import Update
from telegram.ext import ContextTypes
from bot import bot, owner_id
from bot.helper.telegram_helper import Message, Button
from bot.functions.help import func_help
from bot.modules.database.combined_db import find_bot_docs, check_add_user_db


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    args = " ".join(context.args)

    if args == "help":
        await func_help(update, context)
        return

    if not owner_id:
        msg = f"owner_id: <code>{chat.id}</code>\nPlease add owner_id in <code>config.env</code> file then retry. Otherwise bot won't work properly." if chat.type == "private" else "Error <i>owner_id</i> not provided!"
        await Message.reply_message(update, msg)
        return

    if chat.type != "private":
        btn = await Button.ubutton([{"Start me in PM": f"{bot.link}?start=start"}])
        await Message.reply_message(update, f"Hey, {user.first_name}\nStart me in PM!", btn=btn)
        return
    
    _bot = await find_bot_docs()

    bot_pic = _bot.get("bot_pic")
    welcome_img = _bot.get("welcome_img")
    support_chat = _bot.get("support_chat")

    msg = (
        f"Hey, {user.first_name}! I'm {bot.first_name}!\n"
        "I can help you to manage your chat with lots of useful features!\n"
        "Feel free to add me to your chat.\n\n"
        "/help - for bot help\n\n"
        "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
        "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
        "<b>• Developer:</b> <a href='https://t.me/bishalqx980'>bishalqx980</a>"
    )

    if bot.username != "MissCiri_bot":
        msg += "\n\n<i>Cloned bot of @MissCiri_bot</i>"

    btn_data = [{"Add me to your chat": f"{bot.link}?startgroup=help"}]
    if support_chat:
        btn_data.append({"Support Chat": support_chat})
    
    btn = await Button.ubutton(btn_data)
    sent_img = await Message.reply_image(update, bot_pic, msg, btn=btn) if welcome_img and bot_pic else None
    if not sent_img:
        await Message.reply_message(update, msg, btn=btn)
    
    await check_add_user_db(user)
