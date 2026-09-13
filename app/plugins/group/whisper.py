from uuid import uuid4

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.enums import ChatType

from app import bot, COMMAND_PREFIXES
from app.database import MongoDB


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "whisper",
    "commands": ["whisper"], # list of commands including aliases

    "description": (
        "Whisper someone secretly in a public group! Only they can read the message.\n"
        "Usage: `@{bot_username} @username This is a Secret Message!`"
    ),
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Whisper", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}

# collection name for database
WHISPER_COLLECTION_NAME = "whispers"


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    return await message.reply(
        f"**Name :** `{__module__['name']}`\n"
        f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
        f"**Description :** <i>{__module__['description'].format(bot_username=bot.me.username)}</i>\n\n"

        f"**Version :** `{__module__['version']}`\n"
        f"**Author :** `{__module__['author']}`\n\n"

        f"#{__module__['_id']}"
    )


@bot.on_callback_query(filters.regex(r"^whisper:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    whisper_key = query.data.removeprefix("whisper:")

    whisper_data = MongoDB.search(
        WHISPER_COLLECTION_NAME,
        "key",
        whisper_key
    )

    if not whisper_data:
        return await query.edit_message_text(
            "Error: Invalid key.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Send another whisper!", switch_inline_query_current_chat="Demo Secret Message!")
            ]])
        )

    sender_id = whisper_data.get("sender_id")
    receiver_username = whisper_data.get("receiver_username") # without @
    message = whisper_data.get("message")

    if (
        query.from_user.id == sender_id
        or query.from_user.username == receiver_username
    ):
        try:

            await query.answer(
                message,
                True
            )

            # delete the whisper data from database if the receiver get it
            if query.from_user.username == receiver_username:
                MongoDB.delete(
                    WHISPER_COLLECTION_NAME,
                    "key",
                    whisper_key
                )

                await query.edit_message_text(
                    f"<i>@{receiver_username} read the whispered message.</i>",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Send another whisper!", switch_inline_query_current_chat="@username This is a Secret Message!")
                    ]])
                )

        except Exception as e:
            await query.answer(
                str(e),
                True
            )

        

    # Access Denied
    else:
        await query.answer(
            "⚠️ This whisper message isn't for you!",
            True
        )


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
        WHISPER_COLLECTION_NAME,
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
