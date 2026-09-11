from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import Forbidden

from app import bot, COMMAND_PREFIXES
from app.decorators import privatechat_only, admin_require
from app.helpers import CommandArgs


__module__ = {
    "_id": "", # leave it! Auto filled!
    "name": "send",
    "commands": ["send"], # list of commands including aliases

    "description": "Send message to specified user! E.g. reply a message with `/send [username / userid]` or `/send f [username / userid]` to forward.",
    "category": "admin", # check app/__init__.py for HELP_MENU_CATEGORIES
    "button_name": "Send", # Help menu button name (Note: Leaving blank or None will result in no button on help menu)

    "version": "1.0.0", # major.minor.patch
    "author": "http://github.com/bishalqx980"
}


@bot.on_message(filters.command(__module__["commands"], COMMAND_PREFIXES))
@privatechat_only
@admin_require
async def func_(_, message: Message):
    user = message.from_user or message.sender_chat
    re_msg = message.reply_to_message
    # contains str if forward is true and chat_id >> /send f chat_id
    args = CommandArgs(message.text, message.command)

    if not args or not re_msg:
        return await message.reply(
            f"**Name :** `{__module__['name']}`\n"
            f"**Command/s :** {' ༝ '.join(f'/{cmd}' for cmd in __module__['commands'])}\n"
            f"**Description :** <i>{__module__['description']}</i>\n\n"

            f"**Version :** `{__module__['version']}`\n"
            f"**Author :** `{__module__['author']}`\n\n"

            f"#{__module__['_id']}"
        )

    sent_message = await message.reply("Sending...")
    
    forward_confirm = None
    victim_id = args # CHAT_ID or USERNAME

    splited_text = args.split()
    if len(splited_text) == 2:
        forward_confirm, victim_id = splited_text
    
    try:
        # int convert to fix contacts.ResolvePhone error
        try:
            victim_id = int(victim_id)
        except (ValueError, TypeError):
            pass

        if forward_confirm:
            await bot.forward_messages(victim_id, user.id, re_msg.id)
        
        else:
            try:
                victim_chat_info = await bot.get_chat(victim_id)
            except Exception as e:
                return await sent_message.edit(f"Error: {e}")
            
            if victim_chat_info.type == ChatType.PRIVATE:
                text = (
                    f"Message: {re_msg.text.html if re_msg.text else None}\n\n"
                    "<i>Reply to this message to continue conversation!</i>\n"
                    f"||#UID{hex(user.id).upper()}||"
                )
                caption = (
                    f"Message: {re_msg.caption.html if re_msg.caption else None}\n\n"
                    "<i>Reply to this message to continue conversation!</i>\n"
                    f"||#UID{hex(user.id).upper()}||"
                )
            else:
                text = re_msg.text.html if re_msg.text else None
                caption = re_msg.caption.html if re_msg.caption else None
            
            photo = re_msg.photo
            audio = re_msg.audio
            video = re_msg.video
            document = re_msg.document
            voice = re_msg.voice
            video_note = re_msg.video_note
            reply_markup = re_msg.reply_markup

            if text:
                await bot.send_message(
                    victim_id,
                    text,
                    reply_markup=reply_markup
                )

            elif photo:
                await bot.send_photo(
                    victim_id,
                    photo.file_id,
                    caption,
                    reply_markup=reply_markup
                )

            elif audio:
                await bot.send_audio(
                    victim_id,
                    audio.file_id,
                    title=audio.file_name,
                    caption=caption,
                    reply_markup=reply_markup,
                    filename=audio.file_name
                )

            elif video:
                await bot.send_video(
                    victim_id,
                    video.file_id,
                    caption=caption,
                    reply_markup=reply_markup
                )

            elif document:
                await bot.send_document(
                    victim_id,
                    document.file_id,
                    caption,
                    reply_markup=reply_markup,
                    filename=document.file_name
                )
            
            elif voice:
                await bot.send_voice(
                    victim_id,
                    voice.file_id,
                    caption=caption,
                    reply_markup=reply_markup
                )
            
            elif video_note:
                await bot.send_video_note(
                    victim_id,
                    video_note.file_id,
                    reply_markup=reply_markup
                )
            
            else:
                return await sent_message.edit(
                    "Error: Replied content isn't added yet. Stay tuned for future update."
                )
        
        reaction = "👍"
        await sent_message.edit(
            "Message sent!"
        )

    except Forbidden as e:
        reaction = "👎"
        await sent_message.edit(f"Error: {e}")

    except Exception as e:
        reaction = "🤷‍♂"
        await sent_message.edit(f"Error: {e}")

    await message.react(reaction)
