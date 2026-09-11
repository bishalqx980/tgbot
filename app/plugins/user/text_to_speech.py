from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyParameters

from app import bot, COMMAND_PREFIXES, TTS_LANG_CODES_URL
from app.helpers import CommandArgs
from app.modules.tts import TextToSpeech


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "text-to-speech",
    "commands": ["tts"], # list of commands including aliases

    "description": (
        "Text to voice tool. Reply any message with the command to get a voice message!\n"
        "E.g. reply any message with `/tts lang_code` › `/tts en` to get the voice message in English accent."
    ),
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Text-To-Speech", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    re_msg = message.reply_to_message
    lang_code = CommandArgs(message.text, message.command) or "en"

    if not re_msg:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"
    
            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"
    
            f"#{__module__['_id']}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Language code's", url=TTS_LANG_CODES_URL)
            ]])
        )
    
    sent_message = await message.reply("📦 Processing...")

    response = TextToSpeech(re_msg.text or re_msg.caption, lang_code)

    if not response:
        return await sent_message.edit_text(
            "Error: Ohh my head is spinning, I don't know what's going on."
        )

    await sent_message.delete()
    await message.reply_audio(
        response,
        (
            f"**Filename : ** `{response.name}`\n"
            f"**Message ID : ** `{re_msg.id}`\n"
            f"**Lang Code : ** `{lang_code}`"
        ),
        title=response.name,
        reply_parameters=ReplyParameters(
            message_id=re_msg.id
        )
    )
