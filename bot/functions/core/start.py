from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot import ORIGINAL_BOT_USERNAME, ORIGINAL_BOT_ID, ENV_CONFIG, logger
from bot.functions.core.help import func_help
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_add_user

async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    context_args = " ".join(context.args)

    if context_args == "help":
        await func_help(update, context)
        return
    
    if not ENV_CONFIG["owner_id"]:
        await effective_message.reply_text("Warning: Bot OwnerID wasn't provided!")
        return

    if chat.type != ChatType.PRIVATE:
        btn = ButtonMaker.ubutton([{"Start me in PM": f"{context.bot.link}?start=start"}])
        await effective_message.reply_text(f"Hey, {user.first_name}\nStart me in PM!", reply_markup=btn)
        return

    bot_pic = MemoryDB.bot_data.get("bot_pic")
    support_chat = MemoryDB.bot_data.get("support_chat")

    text = (
        f"Hey, {user.first_name}! I'm {context.bot.first_name}!\n"
        "I can help you to manage your chat with lots of useful features!\n"
        "Feel free to add me to your chat.\n\n"
        "/help - for bot help\n\n"
        "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
        "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
        "<b>• Developer:</b> <a href='https://t.me/bishalqx980'>bishalqx980</a>"
    )

    if context.bot.id != ORIGINAL_BOT_ID:
        text += f"\n\n<i>Cloned bot of @{ORIGINAL_BOT_USERNAME}</i>"

    btn_data = [{"Add me to your chat": f"{context.bot.link}?startgroup=help"}]
    if support_chat:
        btn_data.append({"Support Chat": support_chat})
    
    btn = ButtonMaker.ubutton(btn_data)
    if bot_pic:
        try:
            await effective_message.reply_photo(bot_pic, text, reply_markup=btn)
        except Exception as e:
            logger.error(e)
    else:
        await effective_message.reply_text(text, reply_markup=btn)
    
    database_add_user(user)
