from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType

from app import bot, COMMAND_PREFIXES, TL_LANG_CODES_URL
from app.database import MongoDB
from app.helpers import CommandArgs
from app.modules.gtranslator import fetch_langcode, Translate


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "text-translator",
    "commands": ["tr", "translate"], # list of commands including aliases

    "description": (
        "Translate any text to any language!\n"
        "E.g. `/tr text` (to default chat lang) or `/tr lang_code text`\n"
        "OR reply any text with `/tr` (to default chat lang) or `/tr lang_code`\n"
        "Enable auto translator mode for this chat from /settings"
    ),
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Translator", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    chat = message.chat
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message
    text = (re_msg.text or re_msg.caption) if re_msg else None
    args = CommandArgs(message.text, message.command)

    if not text and not args:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Language code's", url=TL_LANG_CODES_URL)
            ]])
        )
    
    to_translate = None
    lang_code = None
    LANG_CODE_LIST = fetch_langcode()
    
    if args:
        words = args.split()
        first_word = words[0]
        if first_word in LANG_CODE_LIST:
            lang_code = first_word
            to_translate = " ".join(words[1:])
    
    if not text and not to_translate and args: # /tr text | lang_code = database
        to_translate = args

    elif text and not to_translate: # /tr (maybe lang_code or maybe not) and replied
        to_translate = text
    
    if not lang_code:
        if chat.type == ChatType.PRIVATE:
            collection_name = MongoDB.USERS
            to_find = "user_id"
            to_match = user.id
        else:
            collection_name = MongoDB.CHATS
            to_find = "chat_id"
            to_match = chat.id

        database_data = MongoDB.search(collection_name, to_find, to_match)
        if not database_data:
            return await message.reply(
                "> **Error:** Chat isn't registered! /reload to fix everthing!"
            )
        
        lang_code = database_data.get("lang")
    
    if not lang_code:
        return await message.reply(
            f"Chat language code wasn't found! Use /{message.command[0]} to get more details or /settings to set chat language.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Language code's", url=TL_LANG_CODES_URL)
            ]])
        )
    
    sent_message = await message.reply("💭 Translating...")

    text = Translate(to_translate, lang_code)
    btn = None

    if text is False:
        text = f"Invalid language code was given! Use /{message.command[0]} to get more details or /settings to set chat language."
        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton("Language code's", url=TL_LANG_CODES_URL)
        ]])

    elif not text:
        text = "Error: Hmm,. Something went wrong!!"
    
    await sent_message.edit_text(text, reply_markup=btn)
