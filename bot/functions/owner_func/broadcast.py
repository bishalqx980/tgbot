import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.helper import BuildKeyboard
from bot.utils.database import MemoryDB
from ..sudo_users import fetch_sudos

async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message

    sudo_users = fetch_sudos()
    if user.id not in sudo_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        sent_message = await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await chat.delete_messages([effective_message.id, sent_message.id])
        return
    
    if not re_msg:
        await effective_message.reply_text("Reply a message to broadcast!")
        return
    
    # variables
    broadcastText = re_msg.text_html # only if the message doesn't contain any video/doc or other things
    broadcastCaption = re_msg.caption_html # message with video/audio/doc etc.

    broadcastPhoto = re_msg.photo[-1].file_id if re_msg.photo else None

    broadcastDocument = re_msg.document.file_id if re_msg.document else None
    broadcastDocument_filename = re_msg.document.file_name if re_msg.document else None

    broadcastVideo = re_msg.video.file_id if re_msg.video else None
    broadcastVideo_note = re_msg.video_note.file_id if re_msg.video_note else None

    broadcastAudio = re_msg.audio.file_id if re_msg.audio else None
    broadcastAudio_filename = re_msg.audio.file_name if re_msg.audio else None

    broadcastVoice = re_msg.voice.file_id if re_msg.voice else None

    broadcastButton = BuildKeyboard.cbutton([
        {"📩 Forward": "broadcast_value_forward", "📌 Pin": "broadcast_value_pin"},
        {"✅ Send": "broadcast_send", "✖️ Close": "misc_close"}
    ])

    broadcastData = {
        "broadcastText": broadcastText,
        "broadcastCaption": broadcastCaption,
        "broadcastPhoto": broadcastPhoto,
        "broadcastDocument": broadcastDocument,
        "broadcastDocument_filename": broadcastDocument_filename,
        "broadcastVideo": broadcastVideo,
        "broadcastVideo_note": broadcastVideo_note,
        "broadcastAudio": broadcastAudio,
        "broadcastAudio_filename": broadcastAudio_filename,
        "broadcastVoice": broadcastVoice,
        # other
        "forward": False,
        "pin": False,
        "is_cancelled": False,
        "replied_message_id": re_msg.id
    }

    MemoryDB.insert("data_center", "broadcast", broadcastData)

    # sening demo preview for owner/sudo
    if broadcastText:
        await effective_message.reply_text(text=broadcastText, reply_markup=broadcastButton)
    elif broadcastPhoto:
        await effective_message.reply_photo(photo=broadcastPhoto, caption=broadcastCaption, reply_markup=broadcastButton)
    elif broadcastDocument:
        await effective_message.reply_document(document=broadcastDocument, caption=broadcastCaption, filename=broadcastCaption, reply_markup=broadcastButton)
    elif broadcastVideo:
        await effective_message.reply_video(video=broadcastVideo, caption=broadcastCaption, reply_markup=broadcastButton)
    elif broadcastVideo_note:
        await effective_message.reply_video_note(video_note=broadcastVideo_note, reply_markup=broadcastButton)
    elif broadcastAudio:
        await effective_message.reply_audio(audio=broadcastAudio, title=broadcastAudio_filename, caption=broadcastCaption, filename=broadcastAudio_filename, reply_markup=broadcastButton)
    elif broadcastVoice:
        await effective_message.reply_voice(voice=broadcastVoice, caption=broadcastCaption, reply_markup=broadcastButton)
    else:
        await effective_message.text("Error: unknown filetype! The file isn't supported for broadcast!")
