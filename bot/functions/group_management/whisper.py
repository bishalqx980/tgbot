from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes
from bot.modules.database import MemoryDB
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.functions.group_management.auxiliary.pm_error import pm_error

async def func_whisper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    secret_message = " ".join(context.args)

    if chat.type == ChatType.PRIVATE:
        await pm_error(context, chat.id)
        return
    
    if not secret_message:
        await effective_message.reply_text("Use <code>/whisper @username message</code>\nor reply user by <code>/whisper message</code>\nE.g. <code>/whisper @bishalqx980 This is a secret message 😜</code>")
        return
    
    try:
        await effective_message.delete()
    except Exception as e:
        await effective_message.reply_text(str(e))
        return

    if re_msg and re_msg.from_user.is_bot:
        await effective_message.reply_text("Whisper isn't for bots...!")
        return
    
    elif re_msg:
        whisper_user = re_msg.from_user.id

    elif secret_message:
        splitted_message = secret_message.split()
        whisper_user = splitted_message[0]
        secret_message = " ".join(splitted_message[1:])

        if not whisper_user.startswith("@"):
            await effective_message.reply_text(f"Give a valid username! <code>{whisper_user}</code> is an invalid username!\nor try to reply the user. /whisper for more details...")
            return
        
        # there is a problem > anonymous admin cant read this ...
        if whisper_user.endswith("bot"):
            await effective_message.reply_text("Whisper isn't for bots...!")
            return
    
    if len(secret_message) > 100:
        await effective_message.reply_text("Whisper message is too long. (Max limit: 100 Characters)")
        return
    
    sent_message = await effective_message.reply_text("Processing...")
    
    data_center = MemoryDB.data_center.get(chat.id)
    if data_center:
        whisper_data = data_center.get("whisper_data")
        if whisper_data:
            whisper_data.update({
                whisper_user: {
                    "user": whisper_user,
                    "message": f"{user.first_name}: {secret_message}"
                }
            })
    
    else:
        data = {
            "whisper_data": {
                whisper_user: {
                    "user": whisper_user,
                    "message": f"{user.first_name}: {secret_message}"
                }
            }
        }

        MemoryDB.insert("data_center", chat.id, data)

    if re_msg:
        whisper_user = re_msg.from_user.mention_html()

    btn = ButtonMaker.cbutton([{"Check the message 👀": "misc_whisper"}])
    await context.bot.edit_message_text(f"Hey, {whisper_user} !! You got a whisper message from {user.mention_html()}.", chat.id, sent_message.id, reply_markup=btn)
