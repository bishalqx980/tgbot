from uuid import uuid4

from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.enums import ChatType

from app import bot
from app.database import MongoDB


class DATA:
    # collection name for database
    WHISPER_COLLECTION_NAME = "whispers"


@bot.on_inline_query()
async def inline_query(_, query: InlineQuery):
    text = query.query.strip()

    if query.chat_type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Group Chat Only",
                    input_message_content=InputTextMessageContent(
                        "This feature is currently available for group chat only. Stay tuned for future updates..."
                    ),
                    id=uuid4(),
                    description="Group Chat Only",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try in a Group chat", switch_inline_query="")
                    ]])
                )
            ]
        )

    if not text:
        # Available inline mode's for the user
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="𝒊 Available inline mode's",
                    input_message_content=InputTextMessageContent(
                        "> **Available inline mode's**\n\n"
                        "• /whisper\n\n"
                        "<i>Note: Use the command for more details. More feature's are coming soon...</i>"
                    ),
                    id=uuid4(),
                    description="Click for more info...!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try inline", switch_inline_query_current_chat="")
                    ]])
                )
            ]
        )

    
    splitted_text = text.split()
    whisper_username = splitted_text[0]
    secret_message = " ".join(splitted_text[1:])

    if not whisper_username.startswith("@"):
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="❗Error: Whisper",
                    input_message_content=InputTextMessageContent(
                        "> **Whisper**\n\n"
                        "Error: Invalid username given!\n"
                        f"Username: `{whisper_username}`\n\n"
                        "<i>Note: Please try again with a valid username.</i>"
                    ),
                    id=uuid4(),
                    description="An error occurred!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")
                    ]])
                )
            ]
        )
    
    if whisper_username.endswith("bot"):
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="❗Error: Whisper",
                    input_message_content=InputTextMessageContent(
                        "> **Whisper**\n\n"
                        "Error: Wisper isn't made for bots!\n"
                        f"Username: `{whisper_username}`\n\n"
                        "<i>Note: Please try again with a valid username.</i>"
                    ),
                    id=uuid4(),
                    description="An error occurred!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")
                    ]])
                )
            ]
        )
    
    if not secret_message:
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="❗Error: Whisper",
                    input_message_content=InputTextMessageContent(
                        "> **Whisper**\n\n"
                        "Error: What do you want to whisper? There is not whisper message!\n"
                        f"Username: `{whisper_username}`\n\n"
                        "<i>Note: Please try again.</i>"
                    ),
                    id=uuid4(),
                    description="Secrect message wasn't given!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")
                    ]])
                )
            ]
        )
    
    if len(secret_message) > 150:
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="❗Error: Whisper",
                    input_message_content=InputTextMessageContent(
                        "> **Whisper**\n\n"
                        "Error: Whisper message is too long. (Max limit: 150 Characters)\n"
                        f"Username: `{whisper_username}`\n\n"
                        "<i>Note: Please try again.</i>"
                    ),
                    id=uuid4(),
                    description="Secrect message is too long!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")
                    ]])
                )
            ]
        )

    whisper_key = uuid4().hex

    MongoDB.insert(
        DATA.WHISPER_COLLECTION_NAME,
        whisper_key,
        {
            "key": whisper_key,
            "sender_id": query.from_user.id,
            "receiver_username": whisper_username.removeprefix("@"), # without @
            "message": secret_message
        }
    )

    await query.answer(
        results=[
            InlineQueryResultArticle(
                title=f"Send the whisper to {whisper_username}!",
                input_message_content=InputTextMessageContent(
                    "> **Whisper**\n\n"
                    f"Hey, {whisper_username}! You got a whisper message from {query.from_user.first_name}."
                ),
                id=uuid4(),
                description="Ready to send.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("💭 Show me the message", f"whisper:{whisper_key}")
                    ],
                    [
                        InlineKeyboardButton("Send another whisper!", switch_inline_query_current_chat="@username This is a Secret Message!")
                    ]
                ])
            )
        ]
    )
