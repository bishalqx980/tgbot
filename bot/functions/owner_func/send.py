import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import Forbidden


from bot.functions.sudo_users import _power_users


async def func_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = effective_message.reply_to_message
    text = " ".join(context.args) # contains something if forward is true and contains victim_id >> /send f chat_id

    power_users = fetch_sudos()
    if user.id not in power_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    if not text or not re_msg:
        msg = (
            "Use <code>/send chat_id</code> by replying a message!\n"
            "<code>/send f chat_id</code> to forward the replied message to chat_id!\n"
            "Returns reaction on message\n"
            "Sent - '👍'\n"
            "Forbidden - '👎'\n"
            "Something went wrong - '🤷‍♂'"
        )
        await effective_message.reply_text(msg)
        return
    
    forward_confirm, victim_id = None, text

    splited_text = text.split()
    if len(splited_text) == 2:
        forward_confirm, victim_id = splited_text

    if forward_confirm:
        sent_msg = await Message.forward_message(victim_id, chat.id, re_msg.id)
    else:
        text = re_msg.text_html
        photo = re_msg.photo
        audio = re_msg.audio
        video = re_msg.video
        document = re_msg.document
        caption = re_msg.caption_html

        # in future update
        # voice = e_msg.voice
        # video_note = e_msg.video_note

        if text:
            sent_msg = await Message.send_message(victim_id, text)
        elif photo:
            sent_msg = await Message.send_image(victim_id, photo[-1].file_id, caption)
        elif audio:
            sent_msg = await Message.send_audio(victim_id, audio.file_id, audio.file_name, caption)
        elif video:
            sent_msg = await Message.send_video(victim_id, video.file_id, caption=caption)
        elif document:
            sent_msg = await Message.send_document(victim_id, document.file_id, document.file_name, caption)
    
    if not sent_msg:
        reaction = "🤷‍♂"
    elif sent_msg == Forbidden:
        reaction = "👎"
    else:
        reaction = "👍"

    await Message.message_reaction(chat.id, e_msg.id, reaction)
