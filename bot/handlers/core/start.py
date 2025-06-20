from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.helpers import create_deep_linked_url
from telegram.error import BadRequest
from bot import ORIGINAL_BOT_USERNAME, ORIGINAL_BOT_ID, logger
from bot.helpers import BuildKeyboard
from bot.utils.database import MemoryDB, database_add_user

async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    if chat.type not in [ChatType.PRIVATE]:
        btn = BuildKeyboard.ubutton([{"Start me in PM": create_deep_linked_url(context.bot.username, "start")}])
        await effective_message.reply_text(f"Hey, {user.first_name}\nStart me in PM!", reply_markup=btn)
        return
    
    # database entry checking if user is registered.
    database_add_user(user)

    show_bot_pic = MemoryDB.bot_data.get("show_bot_pic") # Boolean
    support_chat = MemoryDB.bot_data.get("support_chat")
    photo_file_id = None

    if show_bot_pic:
        try:
            bot_photos = await context.bot.get_user_profile_photos(context.bot.id)
            photo_file_id = bot_photos.photos[0][-1].file_id # the high quality photo file_id
        except:
            pass

    text = (
        f"Hey, {user.first_name}! I'm {context.bot.first_name}!\n\n"
        "I can help you to manage your chat with lots of useful features!\n"
        "Feel free to add me to your chat.\n\n"
        "• /help - Get bot help menu\n\n"
        "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
        "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
        "<b>• Developer:</b> <a href='https://t.me/bishalqx680/22'>bishalqx980</a>"
    )

    if context.bot.id != ORIGINAL_BOT_ID:
        text += f"\n\n<blockquote>Cloned bot of @{ORIGINAL_BOT_USERNAME}</blockquote>"

    btn_data = {"Add me to your chat": create_deep_linked_url(context.bot.username, "help", True)}
    if support_chat:
        btn_data.update({"Support Chat": support_chat})
    
    btn = BuildKeyboard.ubutton([btn_data])

    if photo_file_id:
        try:
            await effective_message.reply_photo(photo_file_id, text, reply_markup=btn)
            return
        except BadRequest:
            pass
        except Exception as e:
            logger.error(e)
    
    # if BadRequest or No Photo or Other error
    await effective_message.reply_text(text, reply_markup=btn)
