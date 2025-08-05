from uuid import uuid4
from base64 import b64decode, b64encode

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from telegram.constants import ChatType

from bot import logger
from bot.helpers import BuildKeyboard
from bot.utils.database import DBConstants, MemoryDB
from bot.modules.utils import Utils

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
        # instruction for user
        instruction_message = (
            "<blockquote><b>Instructions: Available inline modes</b></blockquote>\n\n"

            "<b>• Whisper: send someone a secret message in group chat! Similar command: /whisper</b>\n"
            f"   <i>- Example: <code>{context.bot.name} @bishalqx980 This is a secret message 😜</code></i>\n\n"

            f"<b>• userinfo({user.full_name}): Get your userinfo! Similar command: /info</b>\n"
            f"   <i>- Example: <code>{context.bot.name} info</code></i>\n\n"

            "<b>• Base64 Encode/Decode: Encode/Decode base64 in any chat! Similar commands: /encode | /decode</b>\n"
            f"   <i>- Example: <code>{context.bot.name} base64 data or normal text</code></i>\n\n"

            f"<b>• Instructions: <code>{context.bot.name}</code> - to get this message!</b>\n\n"

            "<b>• Source code:</b> <a href='https://github.com/bishalqx980/tgbot'>GitHub</a>\n"
            "<b>• Report bug:</b> <a href='https://github.com/bishalqx980/tgbot/issues'>Report</a>\n"
            "<b>• Developer:</b> <a href='https://t.me/bishalqx680/22'>bishalqx980</a>"
        )

        results.append(inlineQueryMaker("ℹ️ Instructions", instruction_message, description="Click to see instructions...!"))
        await query.answer(results)
        return
    
    # whisper option: if chat isn't private | This whisper system is temporary store message, use /whisper cmd for permanent message store
    if query.chat_type not in [ChatType.PRIVATE, ChatType.SENDER]:
        splitted_message = message.split()
        whisper_username = splitted_message[0]
        secret_message = " ".join(splitted_message[1:])
        process_whisper = True

        if not whisper_username.startswith("@"):
            process_whisper = False
            results.append(inlineQueryMaker(
                "😮‍💨 Whisper: Error ❌",
                f"<code>{whisper_username}</code> isn't a valid username! Check instructions... Example: <code>{context.bot.name} @username Your Secret message!</code>",
                description=f"{whisper_username}, isn't a valid username!"
            ))
        
        elif whisper_username.endswith("bot"):
            process_whisper = False
            results.append(inlineQueryMaker(
                "😮‍💨 Whisper: Error ❌",
                "Whisper isn't for bots!",
                description="same"
            ))
        
        elif not secret_message:
            process_whisper = False
            results.append(inlineQueryMaker(
                "😮‍💨 Whisper: Error ❌",
                "What do you want to whisper? There is not whisper message!",
                description="same"
            ))
        
        elif len(secret_message) > 150:
            process_whisper = False
            results.append(inlineQueryMaker(
                "😮‍💨 Whisper: Error ❌",
                "Whisper message is too long. (Max limit: 150 Characters)",
                description="same"
            ))
        
        if process_whisper:
            data_center = MemoryDB.data_center.get("whisper_data") or {}
            whispers = data_center.get("whispers") or {}
            whisper_key = Utils.randomString()

            whispers.update({
                whisper_key: {
                    "sender_user_id": user.id,
                    "username": whisper_username, # contains @ prefix
                    "message": secret_message
                }
            })
            
            # Diffrent from normal /whisper cmd
            MemoryDB.insert(DBConstants.DATA_CENTER, "whisper_data", {"whispers": whispers})

            btn = BuildKeyboard.cbutton([
                {"See the message 💭": f"misc_tmp_whisper_{whisper_key}"},
                {"Try Yourself!": "switch_to_inline"}
            ])

            results.append(inlineQueryMaker(
                f"😮‍💨 Whisper: Send to {whisper_username}? ✅",
                f"Hey, {whisper_username}. You got a whisper message from {user.name}.",
                btn,
                f"Send whisper to {whisper_username}!"
            ))
    
    # need to be here after message update otherwise it shows cached info
    user_info = (
        "<blockquote><code>» user.info()</code></blockquote>\n\n"
        
        f"<b>• Full name:</b> <code>{user.full_name}</code>\n"
        f"<b>  » First name:</b> <code>{user.first_name}</code>\n"
        f"<b>  » Last name:</b> <code>{user.last_name}</code>\n"
        f"<b>• Mention:</b> {user.mention_html()}\n"
        f"<b>• Username:</b> {user.name if user.username else ''}\n"
        f"<b>• ID:</b> <code>{user.id}</code>\n"
        f"<b>• Lang:</b> <code>{user.language_code}</code>\n"
        f"<b>• Is bot:</b> <code>{'Yes' if user.is_bot else 'No'}</code>\n"
        f"<b>• Is premium:</b> <code>{'Yes' if user.is_premium else 'No'}</code>"
    )

    results.append(inlineQueryMaker(f"❕ user.info({user.full_name})", user_info, description="See your info...!"))

    # base64 encode / decode
    try:
        b64_decode = b64decode(message).decode("utf-8")
        results.append(inlineQueryMaker("📦 Base64: Decode (base64 to text)", f"<code>{b64_decode}</code>", description=b64_decode)) if b64_decode else None
    except:
        pass

    try:
        b64_encode = b64encode(message.encode("utf-8")).decode("utf-8")
        results.append(inlineQueryMaker("📦 Base64: Encode (text to base64)", f"<code>{b64_encode}</code>", description=b64_encode)) if b64_encode else None
    except:
        pass

    # Final result
    if not results:
        return
    
    await query.answer(results)
