from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
from helper import bot_token, server_url
from helper.telegram_helper import Message
from helper.ping import ping_url
from helper.shortener import shortener_url
from helper.translator import translate
from helper.mongodb import MongoDB


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
    await Message.reply_msg(update, "Hi, this is reply msg")
    
    # await ping_url(update, server_url)
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


async def filter_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text:
        translated_text = translate(text, "bn")
        if translated_text != text:
            await Message.reply_msg(update, translated_text)

        shorted_url = shortener_url(text)
        if shorted_url:
            await Message.reply_msg(update, shorted_url, True)


def main():
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT, filter_text))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print("🤖 Bot Started !!")
    main()
