from telegram import Update, Bot, BotCommand, InlineKeyboardMarkup
from telegram.constants import ParseMode
from helper import bot

class Message:
    async def send_msg(chat_id, msg, btn, disable_web_preview=False):
        if btn:
            reply_markup = InlineKeyboardMarkup(btn)
            await bot.send_message(
                chat_id=chat_id,
                text=msg,
                reply_markup=reply_markup,
                disable_web_page_preview=bool(disable_web_preview),
                parse_mode=ParseMode.HTML
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=msg,
                disable_web_page_preview=bool(disable_web_preview),
                parse_mode=ParseMode.HTML
            )

    
    async def send_img(chat_id, img, caption, btn):
        if btn:
            reply_markup = InlineKeyboardMarkup(btn)
            await bot.send_photo(
                chat_id=chat_id,
                photo=img,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        else:
            await bot.send_photo(
                chat_id=chat_id,
                photo=img,
                caption=caption,
                parse_mode=ParseMode.HTML
            )

    
    async def reply_msg(update: Update, msg, disable_web_preview=False):
        message = update.message
        if message.reply_to_message:
            message_id = message.reply_to_message.message_id
        else:
            message_id = message.message_id

        await update.message.reply_text(
            text=msg,
            disable_web_page_preview=bool(disable_web_preview),
            reply_to_message_id=message_id,
            parse_mode=ParseMode.HTML
        )

