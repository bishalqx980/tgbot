from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import Forbidden
from bot import bot, logger, owner_id
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.misc.message_storage import MessageStorage


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
            await Message.reply_msg(update, f"Hola, {user.mention_html()}!\n<a href='http://t.me/{_bot_info.username}'>Start me</a> in pm to chat with me!")
            return
        elif sent_msg:
            await Message.reply_msg(update, f"Sent in your pm! <a href='http://t.me/{_bot_info.username}'>Check</a>")
            await Message.del_msg(user.id, sent_msg)
    
    _bot = await LOCAL_DATABASE.find("bot_docs")
    if not _bot:
        find = await MongoDB.find("bot_docs", "_id")
        _bot = await MongoDB.find_one("bot_docs", "_id", find[0])
        if not _bot:
            logger.error("_bot not found in db...")
            return
        await LOCAL_DATABASE.insert_data_direct("bot_docs", _bot)
    
    bot_pic = _bot.get("bot_pic")
    welcome_img = _bot.get("welcome_img")
    support_chat = _bot.get("support_chat")

    msg = (
        f"Hi {user.mention_html()}! I'm <a href='https://t.me/{_bot_info.username}'>{_bot_info.first_name}</a>, your all-in-one bot!\n\n"
        "<blockquote>Here's a short summary of what I can do:\n\n"
        "• Get response from ChatGPT\n"
        "• Generate image from your prompt\n"
        "• Download/Search videos from YouTube\n"
        "• Provide movie information\n"
        "• Translate languages\n"
        "• Encode/decode base64\n"
        "• Shorten URLs\n"
        "• Ping any URL\n"
        "• Be your calculator\n"
        "• Echo your message for fun\n"
        "• Take website screenshot\n"
        "• Provide weather information\n"
        "• <b>Group management</b>\n"
        "• & Much more...</blockquote>\n\n"
        "• /help for bot help\n"
        "<i>More Feature coming soon...</i>"
    )

    if _bot_info.username != "MissCiri_bot":
        msg += "\n\nCloned bot of @MissCiri_bot"

    btn_name_1 = ["Add in Group"]
    btn_url_1 = [f"http://t.me/{_bot_info.username}?startgroup=start"]
    btn_name_2 = ["Developer", "Source Code"]
    btn_url_2 = [f"https://t.me/bishalqx980", "https://github.com/bishalqx980/tgbot"]
    btn_name_3 = ["Support Chat"]
    btn_url_3 = [support_chat]

    row_1 = await Button.ubutton(btn_name_1, btn_url_1)
    row_2 = await Button.ubutton(btn_name_2, btn_url_2, True)
    btn = row_1 + row_2

    if support_chat:
        row_3 = await Button.ubutton(btn_name_3, btn_url_3)
        btn = row_1 + row_2 + row_3
    
    if welcome_img and bot_pic:
        await Message.send_img(user.id, bot_pic, msg, btn)
    else:
        await Message.send_msg(user.id, msg, btn)
    
    find_user = await LOCAL_DATABASE.find_one("users", user.id)
    if not find_user:
        find_user = await MongoDB.find_one("users", "user_id", user.id)
        if not find_user:
            data = {
                "user_id": user.id,
                "Name": user.full_name,
                "username": user.username,
                "mention": user.mention_html(),
                "lang": user.language_code,
                "active_status": True
            }

            await MongoDB.insert_single_data("users", data)
            await LOCAL_DATABASE.insert_data("users", user.id, data)
