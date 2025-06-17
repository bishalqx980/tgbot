from uuid import uuid4
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from bot.modules.base64 import BASE64

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query
    # user = query.from_user
    message = query.query
    results = []

    if not message:
        return
    
    try:
        results.append(InlineQueryResultArticle(
            str(uuid4()),
            "Encode: text to base64",
            InputTextMessageContent(str(BASE64.encode(message))),
            description=str(BASE64.encode(message))
        ))
    except:
        pass

    try:
        results.append(InlineQueryResultArticle(
            str(uuid4()),
            "Decode: base64 to text",
            InputTextMessageContent(str(BASE64.decode(message))),
            description=str(BASE64.decode(message))
        ))
    except:
        pass

    if results:
        await query.answer(results)
