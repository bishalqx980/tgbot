from time import time
from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.ai_llm import LLM

async def func_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    prompt = " ".join(context.args)

    if not prompt:
        await effective_message.reply_text("Use <code>/gpt prompt</code>\nE.g. <code>/gpt what is relativity? explain in simple and short way.</code>")
        return
    
    sent_message = await effective_message.reply_text("💭 Generating...")
    
    start_time = time()
    response = await LLM.text_gen(prompt)
    response_time = int(time() - start_time)

    if response:
        text = (
            f"<blockquote expandable>{user.mention_html()}: {prompt}</blockquote>\n"
            f"<blockquote expandable><b>{context.bot.first_name}:</b> {response}</blockquote>\n"
            f"<b>Process time:</b> <code>{response_time}s</code>\n"
            f"<b>UserID:</b> <code>{user.id}</code>"
        )
    else:
        text = "Oops! Something went wrong!"
    
    await context.bot.edit_message_text(text, chat.id, sent_message.id)
