from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.helpers import create_deep_linked_url
from telegram.error import BadRequest
from ... import ORIGINAL_BOT_USERNAME, ORIGINAL_BOT_ID, logger
from ...helper.button_maker import ButtonMaker
from ...modules.database import MemoryDB
from ...modules.database.common import database_add_user

async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type != ChatType.PRIVATE:
        btn = ButtonMaker.ubutton([{"Start me in PM": create_deep_linked_url(context.bot.username, "start")}])
        await effective_message.reply_text(f"Hey, {user.first_name}\nStart me in PM!", reply_markup=btn)
        return

    bot_pic = MemoryDB.bot_data.get("bot_pic")
    support_chat = MemoryDB.bot_data.get("support_chat")

    text = (
        f"Hey, {user.first_name}! I'm {context.bot.first_name}!\n"
        "I can help you to manage your chat with lots of useful features!\n"
        "Feel free to add me to your chat.\n\n"
        "• /help - Get bot help menu\n\n"
        "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
        "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
        "<b>• Developer:</b> <a href='https://t.me/bishalqx980'>bishalqx980</a>"
    )

    if context.bot.id != ORIGINAL_BOT_ID:
        text += f"\n\n<blockquote>Cloned bot of @{ORIGINAL_BOT_USERNAME}</blockquote>"

    btn_data = {"Add me to your chat": create_deep_linked_url(context.bot.username, "help", True)}
    if support_chat:
        btn_data.update({"Support Chat": support_chat})
    
    btn = ButtonMaker.ubutton([btn_data])

    if bot_pic:
        try:
            await effective_message.reply_photo(bot_pic, text, reply_markup=btn)
            return
        except BadRequest:
            pass
        except Exception as e:
            logger.error(e)
    
    # if BadRequest or No Photo
    await effective_message.reply_text(text, reply_markup=btn)

    # database entry checking if user is registered.
    database_add_user(user)
