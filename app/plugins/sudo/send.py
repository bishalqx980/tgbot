from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import BadRequest, Forbidden

from app import bot, COMMAND_PREFIXES
from app.decorators import privatechat_only, sudo_required
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "send",
    "commands": ["send"], # list of commands including aliases

    "description": "Send message to specified user! E.g. reply a message with `/send ( username / userid )`",
    "category": "sudo", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Send", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@sudo_required
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message
    victim_username_or_id = CommandArgs(message.text, message.command)

    if not victim_username_or_id or not re_msg:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )

    sent_message = await message.reply("Sending...")

    victim_username, victim_id = None, None

    try:

        if victim_username_or_id.startswith("@"):
            victim_username = victim_username_or_id
        
        else:

            try:
                victim_id = int(victim_username_or_id)
            except (ValueError, TypeError):
                pass

    except Exception as e:
        return await sent_message.edit(
            f"Error: {e}"
        )
    
    try:
        try:
            victim = await bot.get_chat(victim_username or victim_id)
        except Exception as e:
            return await sent_message.edit(
                f"Error: {e}"
            )
            
        if victim.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            text = re_msg.html_text
            caption = re_msg.caption.html if re_msg.caption else None

        else:
            text = (
                f"Message: {re_msg.html_text}\n\n"
                "<i>Reply to this message to continue conversation!</i>\n"
                f"|| #uid{hex(user.id)} ||"
            )

            caption = (
                f"Message: {re_msg.caption.html if re_msg.caption else None}\n\n"
                "<i>Reply to this message to continue conversation!</i>\n"
                f"|| #uid{hex(user.id)} ||"
            )
        
        photo = re_msg.photo
        audio = re_msg.audio
        video = re_msg.video
        document = re_msg.document
        voice = re_msg.voice
        video_note = re_msg.video_note
        sticker = re_msg.sticker
        reply_markup = re_msg.reply_markup

        if photo:
            await bot.send_photo(
                chat_id=victim.id,
                photo=photo.file_id,
                caption=caption,
                reply_markup=reply_markup
            )

        elif audio:
            await bot.send_audio(
                chat_id=victim.id,
                audio=audio.file_id,
                title=audio.file_name,
                caption=caption,
                reply_markup=reply_markup,
                file_name=audio.file_name
            )

        elif video:
            await bot.send_video(
                chat_id=victim.id,
                video=video.file_id,
                caption=caption,
                reply_markup=reply_markup
            )

        elif document:
            await bot.send_document(
                chat_id=victim.id,
                document=document.file_id,
                caption=caption,
                reply_markup=reply_markup,
                file_name=document.file_name
            )
        
        elif voice:
            await bot.send_voice(
                chat_id=victim.id,
                voice=voice.file_id,
                caption=caption,
                reply_markup=reply_markup
            )
        
        elif video_note:
            await bot.send_video_note(
                chat_id=victim.id,
                video_note=video_note.file_id,
                reply_markup=reply_markup
            )

        elif sticker:
            await bot.send_sticker(
                chat_id=victim_id,
                sticker=sticker.file_id,
                caption=caption,
                reply_markup=reply_markup
            )

        # this condition need to set at bottom to check others first
        elif text:
            await bot.send_message(
                chat_id=victim.id,
                text=text,
                reply_markup=reply_markup
            )
        
        else:
            return await sent_message.edit(
                "Error: Unknown type!"
            )
        
        reaction = "👍"
        await sent_message.edit(
            "Message has been sent!"
        )

    except BadRequest as e:
        reaction = "👎"
        await sent_message.edit(f"Error: {e}")

    except Exception as e:
        reaction = "🤷‍♂"
        await sent_message.edit(f"Error: {e}")

    await message.react(reaction)
