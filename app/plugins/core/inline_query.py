from uuid import uuid4

from pyrogram.types import (
    InlineQuery,
    ChosenInlineResult,
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

    # Group chat only
    if query.chat_type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Group Chat Only",
                    input_message_content=InputTextMessageContent(
                        "This feature is currently available for group chat only.\n"
                        "Stay tuned for future updates..."
                    ),
                    id=str(uuid4()),
                    description="Group Chat Only",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try in a Group chat", switch_inline_query="")
                    ]])
                )
            ],
            cache_time=0,
            is_personal=True
        )

    # No inline query
    if not text:
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="𝒊 Available inline modes",
                    input_message_content=InputTextMessageContent(
                        "> **Available inline modes**\n\n"
                        "• /whisper\n\n"
                        "<i>Note: Use the command for more details. "
                        "More features are coming soon...</i>"
                    ),
                    id=str(uuid4()),
                    description="Click for more info...!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try inline", switch_inline_query_current_chat="")
                    ]])
                )
            ],
            cache_time=0,
            is_personal=True
        )

    splitted_text = text.split()

    whisper_username = splitted_text[0]
    secret_message = " ".join(splitted_text[1:])

    # Username validation
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
                    id=str(uuid4()),
                    description="An error occurred!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")
                    ]])
                )
            ],
            cache_time=0,
            is_personal=True
        )

    # Normalize username
    receiver_username = whisper_username.removeprefix("@").lower()

    # Basic bot username check
    if receiver_username.endswith("bot"):
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="❗Error: Whisper",
                    input_message_content=InputTextMessageContent(
                        "> **Whisper**\n\n"
                        "Error: Whisper isn't made for bots!\n"
                        f"Username: `{whisper_username}`\n\n"
                        "<i>Note: Please try again with a valid username.</i>"
                    ),
                    id=str(uuid4()),
                    description="An error occurred!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")
                    ]])
                )
            ],
            cache_time=0,
            is_personal=True
        )

    # Secret message required
    if not secret_message:
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="❗Error: Whisper",
                    input_message_content=InputTextMessageContent(
                        "> **Whisper**\n\n"
                        "Error: What do you want to whisper? "
                        "There is no whisper message!\n"
                        f"Username: `{whisper_username}`\n\n"
                        "<i>Note: Please try again.</i>"
                    ),
                    id=str(uuid4()),
                    description="Secret message wasn't given!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")
                    ]])
                )
            ],
            cache_time=0,
            is_personal=True
        )

    # Message length
    if len(secret_message) > 150:
        return await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="❗Error: Whisper",
                    input_message_content=InputTextMessageContent(
                        "> **Whisper**\n\n"
                        "Error: Whisper message is too long. "
                        "(Max limit: 150 Characters)\n"
                        f"Username: `{whisper_username}`\n\n"
                        "<i>Note: Please try again.</i>"
                    ),
                    id=str(uuid4()),
                    description="Secret message is too long!",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")
                    ]])
                )
            ],
            cache_time=0,
            is_personal=True
        )

    whisper_key = uuid4().hex

    await query.answer(
        results=[
            InlineQueryResultArticle(
                title=f"Send the whisper to {whisper_username}!",
                input_message_content=InputTextMessageContent(
                    "> **Whisper**\n\n"
                    f"Hey, {whisper_username}! "
                    f"You got a whisper message from "
                    f"{query.from_user.first_name}."
                ),
                # This ID will be received by
                # on_chosen_inline_result()
                id=f"whisper:{whisper_key}",
                description="Ready to send.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "💭 Show me the message",
                            callback_data=f"whisper:{whisper_key}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Send another whisper!",
                            switch_inline_query_current_chat=(
                                "@username This is a Secret Message!"
                            )
                        )
                    ]
                ])
            )
        ],
        cache_time=0,
        is_personal=True
    )


@bot.on_chosen_inline_result()
async def chosen_inline_result(_, result: ChosenInlineResult):

    result_id = result.result_id

    if result_id.startswith("whisper:"):
        whisper_key = result_id.removeprefix("whisper:")

        # The original query is still available here.
        text = result.query.strip()

        if not text:
            return
        
        splitted_text = text.split()

        if len(splitted_text) < 2:
            return

        whisper_username = splitted_text[0]

        if not whisper_username.startswith("@"):
            return

        secret_message = " ".join(splitted_text[1:])

        if not secret_message:
            return
        
        receiver_username = whisper_username.removeprefix("@").lower()

        MongoDB.insert(
            DATA.WHISPER_COLLECTION_NAME,
            whisper_key,
            {
                "key": whisper_key,
                "sender_id": result.from_user.id,
                "receiver_username": receiver_username, # without @
                "message": secret_message
            }
        )
