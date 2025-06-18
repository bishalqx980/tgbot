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
        bot_source_info = (
            "<blockquote><b>Source info</b></blockquote>\n\n"

            "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
            "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
            "<b>• Developer:</b> <a href='https://t.me/bishalqx680/22'>bishalqx980</a>"
        )

        results.append(inlineQueryMaker(f"What's up, {user.full_name} 🤗!!", "Huh, not funny 😒!!", description="Don't click!"))
        results.append(inlineQueryMaker("bot.source.info()", bot_source_info, description="Loading... (click/tap to see)"))
        await query.answer(results)
        return
    
    # need to be here after message update otherwise it shows cached userID
    results.append(inlineQueryMaker("Your UserID", f"<code>{user.id}</code>", description=user.id))
    # need to be here bcz of cached
    user_info = (
        "<blockquote><code>» user.info()</code></blockquote>\n\n"
        
        f"<b>• Full name:</b> <code>{user.full_name}</code>\n"
        f"<b>  » First name:</b> <code>{user.first_name}</code>\n"
        f"<b>  » Last name:</b> <code>{user.last_name}</code>\n"
        f"<b>• Mention:</b> {user.mention_html()}\n"
        f"<b>• Username:</b> {user.name if user.username else 'Huh, not funny 😒!!'}\n"
        f"<b>• ID:</b> <code>{user.id}</code>\n"
        f"<b>• Lang:</b> <code>{user.language_code}</code>\n"
        f"<b>• Is bot:</b> <code>{'Yes' if user.is_bot else 'Huh, not funny 😒!!'}</code>\n"
        f"<b>• Is premium:</b> <code>{'Yes' if user.is_premium else 'Huh, not funny 😒!!'}</code>"
    )

    results.append(inlineQueryMaker(f"user.info(): {user.full_name}", user_info, description="See your info"))

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
