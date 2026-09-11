from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app import bot, COMMAND_PREFIXES
from app.decorators import (
    groupchat_only,
    bot_admin,
    bot_can_pin_messages,
    user_admin,
    user_can_pin_messages
)


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "unpin",
    "commands": ["unpin", "sunpin"], # list of commands including aliases

    "description": "Unpin replied pinned message or all pinned messages.",
    "category": "group", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Unpin", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@groupchat_only
@user_admin
@user_can_pin_messages
@bot_admin
@bot_can_pin_messages
async def func_(_, message: Message):
    re_msg = message.reply_to_message

    command = message.command[0]
    is_silent = False
    
    try:

        if command.startswith("s"):
            is_silent = True
            await message.delete()
        
    except:
        pass
    
    if not re_msg:
        return await message.reply_text(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🧹 Unpin all messages", f"unpin:all_messages:{message.from_user.id if message.from_user else 'anonymous'}"),
                InlineKeyboardButton("✘ Close", "unpin:close")
            ]])
        )
    
    try:

        await re_msg.unpin()

        if not is_silent:
            await message.reply_text(
                f"Message [{re_msg.id}]({re_msg.link}) is unpinned in this chat by {message.from_user.mention if message.from_user else 'Anonymous'}."
            )
        
    except Exception as e:
        return await message.reply_text(
            f"Error: {e}"
        )


@bot.on_callback_query(filters.regex(r"^unpin:[A-Za-z0-9]+"))
async def query_(_, query: CallbackQuery):
    query_data = query.data.removeprefix("unpin:")

    if query_data.startswith("all_messages:"):
        admin_id = query_data.removeprefix("all_messages:")

        if admin_id == "anonymous":
            return await query.answer(
                "❌ This feature is unavailable for anonymous admin.",
                True
            )

        if str(query.from_user.id) != admin_id:
            return await query.answer(
                "❌ This is not your call buddy. Try to send the command yourself.",
                True
            )
        
        try:

            await bot.unpin_all_chat_messages(
                query.message.chat.id
            )

            await query.edit_message_text(
                f"All pinned messages of this chat have been unpinned by {query.from_user.mention}."
            )

            await query.answer("✅ Successful!", True)
            
        except Exception as e:
            return await query.edit_message_text(
                f"Error: {e}"
            )

    elif query_data == "close":
        try:
            await query.answer()
        except:
            pass

        try:
            message_id = query.message.id
            await bot.delete_messages(query.message.chat.id, [message_id, message_id - 1])
        except:
            try:
                await query.delete_message()
            except:
                pass
        return
