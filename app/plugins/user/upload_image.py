from uuid import uuid4

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions

from app import bot, COMMAND_PREFIXES
from app.modules.api.freeimagehost import UploadImage


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "imagehost",
    "commands": ["imgtolink", "uploadimg", "itl", "uimg"], # list of commands including aliases

    "description": "Upload an image to public hosting server! Get a url of the uploaded image. Reply an image with the command.",
    "category": "user", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Upload Image", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
async def func_(_, message: Message):
    re_msg = message.reply_to_message

    if re_msg:
        if re_msg.photo:
            image = re_msg.photo.file_id
        elif re_msg.document and "image" in re_msg.document.mime_type:
            image = re_msg.document.file_id
        else:
            image = None

    if not re_msg or not image:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )
    
    sent_message = await message.reply("💭 Please wait...")

    image_buffer = await re_msg.download(
        f"{uuid4().hex}.png",
        in_memory=True
    )

    if not image_buffer:
        return await sent_message.edit_text(
            "Error: Unable to read the image data. please try again!"
        )
    
    await sent_message.edit_text("📤 Uploading...")

    response = await UploadImage(image_buffer.getvalue())

    if not response:
        return await sent_message.edit_text("Error: Huh? I don't what is happening with me!")
    elif isinstance(response, str):
        return await sent_message.edit_text(f"Error: {response}")
    
    status_code = response["status_code"]
    if status_code != 200:
        error_message = response.get("error", {}).get("message", "???")
        return await sent_message.edit_text(f"Error: {error_message}")

    image_data = response["image"]

    image_url = image_data.get("url")
    image_width = image_data.get("width")
    image_height = image_data.get("height")
    image_size = image_data.get("size_formatted")
    image_mime = image_data.get("image", {}).get("mime")
    
    await sent_message.edit_text(
        "> **Image Details**\n\n"

        f"**➜ URL:** <a href='{image_url}'>◊ View Image ◊</a>\n"
        f"**➜ Width:** `{image_width}px`\n"
        f"**➜ Height:** `{image_height}px`\n"
        f"**➜ Size:** `{image_size}`\n"
        f"**➜ Mime:** `{image_mime}`",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("View 🖼️", url=image_url),
            InlineKeyboardButton("Copy Link", copy_text=image_url)
        ]]),
        link_preview_options=LinkPreviewOptions(
            is_disabled=False,
            prefer_small_media=True,
            show_above_text=True
        )
    )
