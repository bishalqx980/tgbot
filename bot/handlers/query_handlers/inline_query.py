from uuid import uuid4
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from bot import logger
from bot.helpers import BuildKeyboard
from bot.modules.base64 import BASE64

def inlineQueryMaker(title, message, reply_markup=None, description=None):
    """
    :param description: Type `same` if you want to keep the description same as message!
    """
    if not reply_markup:
        reply_markup = BuildKeyboard.cbutton([{"Try inline": "switch_to_inline"}])
    
    try:
        content = InlineQueryResultArticle(
            str(uuid4()),
            title=title,
            input_message_content=InputTextMessageContent(message),
            reply_markup=reply_markup,
            description=message if description == "same" else description
        )

        return content
    except Exception as e:
        logger.error(e)
        return


async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query
    user = query.from_user
    message = query.query
    results = []

    if not message:
        results.append(inlineQueryMaker("Type your message/text", "Type your message/text"))
        await query.answer(results)
        return
    
    # userID
    results.append(inlineQueryMaker("Your UserID", f"<code>{user.id}</code>", description=user.id))
    # base64 encode / decode
    b64_encode = BASE64.encode(message)
    b64_decode = BASE64.decode(message)

    if b64_encode:
        results.append(inlineQueryMaker("Base64: Encode (text to base64)", f"<code>{b64_encode}</code>", description=b64_encode))
    
    if b64_decode:
        results.append(inlineQueryMaker("Base64: Decode (base64 to text)", f"<code>{b64_decode}</code>", description=b64_decode))

    if not results:
        return
    
    await query.answer(results)
