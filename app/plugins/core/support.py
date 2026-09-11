from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, config, logger, COMMAND_PREFIXES
from app.decorators import privatechat_only

__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "support",
    "commands": ["support", "report"], # list of commands including aliases

    "description": "Contact with us!",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Support", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


SUPPORT_LIST = set()

def support_filter(_, __, message: Message):
    user = message.from_user or message.sender_chat
    return user and user.id in SUPPORT_LIST

support_waiting = filters.create(support_filter)


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat

    await message.reply(
        f"Hey, {user.mention}!\n"
        "Please send your **report** or **support request** below. We'll review it and get back to you as soon as possible. 💬\n\n"
        "> **Note:** Message should be related to this bot. And we don't provide any support for ban, mute or other things related to groups managed by this bot.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Cancel", "support:cancel")
        ]])
    )

    SUPPORT_LIST.add(user.id)


@bot.on_callback_query(filters.regex(r"^support:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    if query.data == "support:cancel":
        SUPPORT_LIST.discard(query.from_user.id)
        await query.answer("Support ticket has been closed!", True)
        await query.edit_message_text("Support ticket has been closed!")


@bot.on_message(filters.text & support_waiting)
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat

    SUPPORT_LIST.discard(user.id)

    try:
        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton("User Profile", user_id=user.id)
        ]]) if user.username else None

        await bot.send_message(
            config.owner_id,
            (
                f"**Name:** {user.mention}\n"
                f"**UserID:** `{user.id}`\n"
                f"**Message:** {message.html_text}\n\n"
                "<i>Reply to this message to continue conversation! or use /send</i>\n"
                f"|| #uid{hex(user.id)} ||"
            ),
            reply_markup=btn
        )

        response_text = "Ticket has been submitted. We'll get back to you as soon as possible."
    except Exception as e:
        logger.error(e)
        response_text = (
            "Something went wrong!\n"
            f"Error: {e}"
        )

    await message.reply_text(response_text)
