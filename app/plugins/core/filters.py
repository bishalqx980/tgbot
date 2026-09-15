from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import BadRequest, Forbidden

from app import bot, config, logger


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
                victim_id = int(replied_text.split("#uid")[1].strip(), 16) # base 16: hex
                text = ""
                caption = ""
                btn = None

                # Add userinfo if the message is sending to owner/support team
                if user.id != config.owner_id:
                    text += (
                        f"Name: {user.mention}\n"
                        f"UserID: `{user.id}`\n"
                    )

                    caption += (
                        f"Name: {user.mention}\n"
                        f"UserID: `{user.id}`\n"
                    )

                    btn = InlineKeyboardMarkup([[
                        InlineKeyboardButton("User Profile", user_id=user.id)
                    ]]) if user.username else None
                
                # Common message for owner & user
                text += (
                    f"Message: {message.html_text}\n\n"
                    "<i>Reply to this message to continue conversation!</i>\n"
                    f"|| #uid{hex(user.id)} ||"
                )
    
                caption += (
                    f"Message: {message.caption.html if message.caption else None}\n\n"
                    "<i>Reply to this message to continue conversation!</i>\n"
                    f"|| #uid{hex(user.id)} ||"
                )
            
                photo = message.photo
                audio = message.audio
                video = message.video
                document = message.document
                voice = message.voice
                video_note = message.video_note
                sticker = message.sticker
        
                if photo:
                    await bot.send_photo(
                        chat_id=victim_id,
                        photo=photo.file_id,
                        caption=caption,
                        reply_markup=btn
                    )
        
                elif audio:
                    await bot.send_audio(
                        chat_id=victim_id,
                        audio=audio.file_id,
                        title=audio.file_name,
                        caption=caption,
                        reply_markup=btn,
                        file_name=audio.file_name
                    )
        
                elif video:
                    await bot.send_video(
                        chat_id=victim_id,
                        video=video.file_id,
                        caption=caption,
                        reply_markup=btn
                    )
        
                elif document:
                    await bot.send_document(
                        chat_id=victim_id,
                        document=document.file_id,
                        caption=caption,
                        reply_markup=btn,
                        file_name=document.file_name
                    )
                
                elif voice:
                    await bot.send_voice(
                        chat_id=victim_id,
                        voice=voice.file_id,
                        caption=caption,
                        reply_markup=btn
                    )
                
                elif video_note:
                    await bot.send_video_note(
                        chat_id=victim_id,
                        video_note=video_note.file_id,
                        reply_markup=btn
                    )

                elif sticker:
                    await bot.send_sticker(
                        chat_id=victim_id,
                        sticker=sticker.file_id,
                        caption=caption,
                        reply_markup=btn
                    )
        
                # this condition need to set at bottom to check others first
                elif text:
                    await bot.send_message(
                        chat_id=victim_id,
                        text=text,
                        reply_markup=btn
                    )
                
                else:
                    return await message.reply(
                        "Error: Unknown type!"
                    )
                
                reaction = "👍"

            except BadRequest as e:
                logger.error(e)
                reaction = "👎"

            except Exception as e:
                logger.error(e)
                reaction = "🤷‍♂"
            # Confirm that message is sent or not
            await message.react(reaction)
