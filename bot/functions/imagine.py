import os
import time
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.ai_llm import LLM

async def func_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    prompt = " ".join(context.args)

    if not prompt:
        await Message.reply_message(update, "Use <code>/imagine prompt</code>\nE.g. <code>/imagine A cat and a dog playing</code>")
        return
    
    sent_msg = await Message.reply_message(update, "🎨 Generating...")
    start_time = time.time()
    response = await LLM.imagine(prompt, f"imagine_{user.id}")
    response_time = int(time.time() - start_time)
    if not response:
        await Message.edit_message(update, "Oops! Please try again or report the issue.", sent_msg)
        return
    
    caption = (
        f"<b>📝 Prompt:</b> <code>{prompt}</code>\n"
        f"<b>⏳ R.time:</b> <code>{response_time}s</code>\n"
        f"<b>🗣 Req by:</b> {user.mention_html()} | <code>{user.id}</code>"
    )

    await Message.send_image(chat.id, response, caption, e_msg.id)
    await Message.delete_message(chat.id, sent_msg)

    # Removing the image file
    try:
        os.remove(response)
    except Exception as e:
        logger.error(e)
