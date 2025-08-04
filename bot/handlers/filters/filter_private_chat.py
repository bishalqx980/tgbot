from telegram import Update, ReactionTypeEmoji
from telegram.ext import ContextTypes
from telegram.error import Forbidden

from bot import TL_LANG_CODES_URL, config
from bot.helpers import BuildKeyboard
from bot.utils.database import DBConstants, database_search

from .edit_database import edit_database
from .auto_translate import autoTranslate

async def filter_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    # Support Conversation
    if message.reply_to_message:
        replied_message = message.reply_to_message
        if "#uid" in [replied_message.text or replied_message.caption]:
            try:
                support_conv_uid = int(replied_message.text.split("#uid")[1].strip(), 16) # base 16: hex
                text = ""
                btn = None
                # if user sending message to owner/support-team then add userinfo
                if user.id != config.owner_id:
                    text += (
                        f"Name: {user.mention_html()}\n"
                        f"UserID: <code>{user.id}</code>\n"
                    )

                    btn = BuildKeyboard.ubutton([{"User Profile": f"tg://user?id={user.id}"}]) if user.username else None
                
                # Common text for owner & user
                text += (
                    f"Message: {message.text_html}\n\n"
                    "<i>Reply to this message to continue conversation!</i>\n"
                    f"<tg-spoiler>#uid{hex(user.id)}</tg-spoiler>"
                )

                await context.bot.send_message(support_conv_uid, text, reply_markup=btn)
                reaction = "👍"
            except Forbidden:
                reaction = "👎"
            except:
                reaction = "🤷‍♂"
            # Confirm that message is sent or not
            await message.set_reaction([ReactionTypeEmoji(reaction)])
    
    is_editing = edit_database(chat.id, user.id, message)
    if is_editing:
        return
    
    user_data = database_search(DBConstants.USERS_DATA, "user_id", user.id)
    if not user_data:
        await message.reply_text("<blockquote><b>Error:</b> Chat isn't registered! Remove/Block me from this chat then add me again!</blockquote>")
        return
    
    # Echo message
    if user_data.get("echo"):
        await message.reply_text(message.text_html or message.caption_html)
    
    # Auto Translator
    auto_tr = user_data.get("auto_tr")
    chat_lang = user_data.get("lang")

    if auto_tr and not chat_lang:
        btn = BuildKeyboard.ubutton([{"Language code's": TL_LANG_CODES_URL}])
        await message.reply_text("Chat language code wasn't found! Use /settings to set chat language.", reply_markup=btn)
    
    elif auto_tr:
        await autoTranslate(message, user, chat_lang)
