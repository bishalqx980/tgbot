import os
from time import time
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.modules.ai_llm import LLM

async def func_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    prompt = " ".join(context.args)

    if not prompt:
        await effective_message.reply_text("Use <code>/imagine prompt</code>\nE.g. <code>/imagine A cat and a dog playing</code>")
        return
    
    sent_message = await effective_message.reply_text("🎨 Generating...")
    start_time = time()
    response = await LLM.imagine(prompt, f"imagine_{user.id}")
    response_time = int(time() - start_time)
    if not response:
        await context.bot.edit_message_text("Oops! Something went wrong!", chat.id, sent_message.id)
        return
    
    caption = (
        f"<b>💭 Prompt:</b> <code>{prompt}</code>\n"
        f"<b>⏳ R.time:</b> <code>{response_time}s</code>\n"
        f"<b>🗣 Req by:</b> {user.mention_html()} | <code>{user.id}</code>"
    )

    await context.bot.delete_message(chat.id, sent_message.id)
    await effective_message.reply_photo(response, caption)

    # Removing the image file
    try:
        os.remove(response)
    except Exception as e:
        logger.error(e)
