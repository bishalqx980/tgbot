from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
from helper import bot_token, server_url
from helper.mongodb import MongoDB
from helper.telegram_helper import Message
from helper.ping import ping_url
from helper.shortener import shortener_url
from helper.translator import translate
from helper.base64 import decode_b64, encode_b64


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    # await Message.send_msg(chat_id, "Hi, this is send msg", btn=None)
    # await Message.send_msg(chat_id, "Hi this is a btn message", btn)
    # await Message.send_img(chat_id, img, "<b>python-telegram-bot==20.7</b>", btn=None)
    # await Message.send_img(chat_id, img, "<b>python-telegram-bot==20.7</b>", btn)
    
    ping = ping_url(server_url)
    await Message.reply_msg(update, f"URL: {ping[0]}\nTime(ms): {ping[1]}\nResponse: {ping[2]}")

    # MongoDB.info_db()
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

async def filter_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    caption = update.message.caption
    content = text if text else caption

    ping = ping_url(content)
    await Message.reply_msg(update, f"URL: {ping[0]}\nTime(ms): {ping[1]}\nResponse: {ping[2]}")

    if content:
        translated_text = translate(content, "bn")
        if translated_text != content:
            await Message.reply_msg(update, translated_text)

        shorted_url = shortener_url(content)
        if shorted_url:
            await Message.reply_msg(update, shorted_url, True)
        
        encode = encode_b64(content)
        decode = decode_b64(content)
        await Message.reply_msg(update, f"Encode: {encode}")
        await Message.reply_msg(update, f"Decode: {decode}")



def main():
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.ALL, filter_text))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print("🤖 Bot Started !!")
    main()
