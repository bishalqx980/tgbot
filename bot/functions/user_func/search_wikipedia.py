import wikipedia
from time import time
from telegram import Update
from telegram.ext import ContextTypes

async def func_wiki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    query = " ".join(context.args)

    if not query:
        await effective_message.reply_text("Use <code>/wiki query</code>\nE.g. <code>/wiki PlayStation</code>")
        return
    
    sent_message = await effective_message.reply_text("💭 Searching...")
    start_time = time()

    try:
        response = wikipedia.summary(query)
    except Exception as e:
        await context.bot.edit_message_text(str(e), chat.id, sent_message.id)
        return
    
    response_time = f"{(time() - start_time):.2f}s"

    text = (
        f"<blockquote expandable>{user.mention_html()}: {query}</blockquote>\n"
        f"<blockquote expandable><b>{context.bot.first_name}:</b> {response}</blockquote>\n"
        f"<b>Process time:</b> <code>{response_time}</code>\n"
        f"<b>UserID:</b> <code>{user.id}</code>"
    )

    await context.bot.edit_message_text(text, chat.id, sent_message.id)
