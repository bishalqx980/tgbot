from uuid import uuid4

from pyrogram import filters
from pyrogram.types import Message

from app import bot, COMMAND_PREFIXES
from app.modules.qr import QR


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "decodeqr",
    "commands": ["decodeqr", "decqr"], # list of commands including aliases

    "description": "Reply any QR-code-image to decode the QR-code!",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Decode QR", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message

    if not re_msg or not (re_msg.photo or re_msg.document):
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"
    
            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"
    
            f"#{__module__['_id']}"
        )
    
    if re_msg.document and not "image" in re_msg.document.mime_type:
        return await message.reply(
            "Hey, You have replied the wrong file. It's not an image file!"
        )
    
    image = re_msg.photo or re_msg.document

    if isinstance(image, tuple):
        image = image[-1]
    
    if re_msg.photo:
        sent_message = await message.reply_photo(image.file_id, caption="Please wait...")
    else:
        sent_message = await message.reply_document(image.file_id, caption="Please wait...")

    # Reading the image file in memory
    image_buffer = await re_msg.download(f"{uuid4().hex}.png", in_memory=True)

    decoded_data = QR.DecodeQR(image_buffer)

    if decoded_data:
        text = (
            f"**Decoded Data:** `{decoded_data.data.decode()}`\n"
            f"**Type:** `{decoded_data.type}`\n"
            f"**Req by:** {user.mention} | `{user.id}`"
        )
    else:
        text = "Error: Damn! Sorry I don't know what happened!"

    await sent_message.edit_caption(text)
