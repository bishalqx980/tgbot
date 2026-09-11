from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import Forbidden

from app import bot, config


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "filters",
    "commands": [], # list of commands including aliases

    "description": "",
    "category": "", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.all, group=-1)
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message

    if re_msg:
        replied_text = re_msg.text or re_msg.caption

        if replied_text and "#uid" in replied_text:
            try:
                user_id = int(replied_text.split("#uid")[1].strip(), 16) # base 16: hex
                text = ""
                btn = None

                # if user sending message to owner/support-team then add userinfo
                if user.id != config.owner_id:
                    text += (
                        f"**Name:** {user.mention}\n"
                        f"**UserID:** `{user.id}`\n"
                    )

                    btn = InlineKeyboardMarkup([[
                        InlineKeyboardButton("User Profile", user_id=user.id)
                    ]]) if user.username else None
                
                # Common text for owner & user
                text += (
                    f"**Message:** {message.html_text}\n\n"
                    "<i>Reply to this message to continue conversation!</i>\n"
                    f"|| #uid{hex(user.id)} ||"
                )

                await bot.send_message(
                    user_id,
                    text,
                    reply_markup=btn
                )

                reaction = "👍"

            except Forbidden:
                reaction = "👎"

            except:
                reaction = "🤷‍♂"
            # Confirm that message is sent or not
            await message.react(reaction)
