import time
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.ai_llm import LLM

async def func_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    prompt = " ".join(context.args)

    if not prompt:
        await Message.reply_message(update, "Use <code>/gpt prompt</code>\nE.g. <code>/gpt make me laugh</code>")
        return
    
    sent_msg = await Message.reply_message(update, "📝 Generating...")
    start_time = time.time()
    response = await LLM.text_gen(prompt)
    response_time = int(time.time() - start_time)
    if response:
        msg = (
            f"<b>📝 Prompt:</b> <code>{prompt}</code>\n"
            f"<b>⏳ R.time:</b> <code>{response_time}s</code>\n"
            f"<b>🗣 Req by:</b> {user.mention_html()} | <code>{user.id}</code>\n"
            f"<b>Response: <blockquote>{response}</blockquote></b>"
        )
    else:
        msg = "Oops! Please try again or report the issue."
    
    await Message.edit_message(update, msg, sent_msg)
