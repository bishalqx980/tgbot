from time import time
from telegram import Update
from telegram.ext import ContextTypes
from bot.modules import llm

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
    response = await llm.imagine(prompt)
    response_time = f"{(time() - start_time):.2f}s"

    if not response:
        await sent_message.edit_text("Oops! Something went wrong!")
        return
    
    caption = (
        f"<blockquote>{user.mention_html()}: {prompt}</blockquote>\n"
        f"<b>Process time:</b> <code>{response_time}</code>\n"
        f"<b>UserID:</b> <code>{user.id}</code>"
    )

    await sent_message.delete()
    await effective_message.reply_photo(response, caption)
