import asyncio
from telegram import Update, InlineKeyboardButton, InputMedia
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot import bot_token, owner_id, server_url
from bot.mongodb import MongoDB
from bot.helper.telegram_helper import Message
from bot.ping import ping_url
from bot.shortener import shortener_url
from bot.translator import translate
from bot.base64 import decode_b64, encode_b64
from bot.omdb_movie_info import get_movie_info
from bot.utils import calc
from bot.helper.tgmsg_storage import MsgStorage


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    img = 'https://docs.python-telegram-bot.org/en/v20.7/_static/ptb-logo_1024.png'

    btn = [
        [
            InlineKeyboardButton("python-telegram-bot", img),
            InlineKeyboardButton("Google", "https://google.com")
        ],
        [
            InlineKeyboardButton("YouTube", "https://youtube.com")
        ]
    ]

    await Message.send_msg(chat_id, "Hi, this is send msg")
    await Message.send_msg(chat_id, "Hi this is a btn message", btn)
    await Message.send_img(chat_id, img, "<b>python-telegram-bot==20.7</b>", btn=None)
    await Message.send_img(chat_id, img, "<b>python-telegram-bot==20.7</b>", btn)
    
    ping = ping_url(server_url)
    x = await Message.reply_msg(update, f"URL: {ping[0]}\nTime(ms): {ping[1]}\nResponse: {ping[2]}")
    y = await Message.send_img(update.effective_chat.id, img, "python telegram bot library")
    z = await Message.send_msg(update.effective_chat.id, "Hi from send_mg...") 
    await asyncio.sleep(2)
    
    await Message.send_msg(update.effective_chat.id, "Hi", btn)
    for msg in [x, y, z]:
        await Message.edit_msg(update, "Message Edited...", msg)

    """ info = MongoDB.find("users", "user_id")
    await Message.reply_msg(update, info) """

    """ 
    user = update.effective_user
    data = {
        "name": user.full_name,
        "user_id": user.id,
        "user_mention": user.mention_html(),
        "user_name": user.username
    }

    check_db = MongoDB.find_one("users", "user_id", data["user_id"])
    if check_db:
        pass
    else:
        MongoDB.insert_single_data("users", data)
    """

async def func_filter_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    caption = update.message.caption
    content = text if text else caption

    """ ping = ping_url(content)
    if ping:
        await Message.reply_msg(update, f"URL: {ping[0]}\nTime(ms): {ping[1]}\nResponse: {ping[2]}") """

    if content:
        """ translated_text = translate(content, "bn")
        if translated_text != content:
            await Message.reply_msg(update, translated_text)

        shorted_url = shortener_url(content)
        if shorted_url:
            await Message.reply_msg(update, shorted_url, True)
        
        encode = encode_b64(content)
        decode = decode_b64(content)
        await Message.reply_msg(update, f"Encode: {encode}")
        await Message.reply_msg(update, f"Decode: {decode}") """

        movie_info = get_movie_info(content)
        if movie_info:
            x = MsgStorage.msg_movie_info(movie_info)
            await Message.send_img(update.effective_chat.id, movie_info[0], x)


async def func_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    echo_msg = " ".join(context.args)
    if echo_msg == "on":
        await Message.reply_msg(update, echo_msg)
    else:
        await Message.reply_msg(update, "on not mentioned")


async def func_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = " ".join(context.args)
    if url:
        await Message.reply_msg(update, ping_url(url))


async def func_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    math = " ".join(context.args)
    if math:
        await Message.reply_msg(update, calc(math))


async def func_dbinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    x = MongoDB.info_db()

    print(x)


async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    replied_msg = update.message.reply_to_message
    if user_id == int(owner_id):
        if replied_msg:
            msg = replied_msg.text
        else:
            await Message.reply_msg(update, "Reply a message to broadcard!")
            return
        
        user_ids = MongoDB.find("users", "user_id")
        x = MongoDB.info_db("users")

        sent_count = 0
        for user_id in user_ids:
            try:
                await Message.send_msg(user_id, msg)
                await Message.reply_msg(update, "I will notify you once job done!")
                sent_count += 1
            except Exception as e:
                print(f"Error Broadcast: {e}")
        await Message.send_msg(owner_id, f"Sent: {sent_count}\nTotal User: {x[1]}")
    else:
        await Message.reply_msg(update, "This command is not for you!")


def main():
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", func_start))
    application.add_handler(CommandHandler("echo", func_echo))
    application.add_handler(CommandHandler("ping", func_ping))
    application.add_handler(CommandHandler("calc", func_calc))
    application.add_handler(CommandHandler("db", func_dbinfo))
    application.add_handler(CommandHandler("x", func_broadcast))

    application.add_handler(MessageHandler(filters.ALL, func_filter_all))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print("🤖 Bot Started !!")
    main()
