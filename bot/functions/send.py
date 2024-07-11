import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import Forbidden
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users


async def func_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = update.message.reply_to_message
    text = " ".join(context.args)

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "Access denied!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, f"Boss you are in public chat!")
        await asyncio.sleep(3)
        del_msg_ids = [e_msg.id, e_msg.id + 1]
        await asyncio.gather(*(Message.del_msg(chat.id, msg_id=msg_id) for msg_id in del_msg_ids))
        return
    
    if not text or not re_msg:
        await Message.reply_msg(update, "Use <code>/send chat_id</code> by replying a message!\n<code>/send f chat_id</code> to forward the replied message to chat_id!")
        return
    
    forward_confirm, chat_id = None, text

    splited_text = text.split()
    if len(splited_text) == 2:
        forward_confirm, chat_id = splited_text
    
    msg = re_msg.text_html or re_msg.caption_html if re_msg else None

    if forward_confirm:
        sent_msg = await Message.forward_msg(chat_id, chat.id, re_msg.id)
    else:
        if re_msg.text_html:
            sent_msg = await Message.send_msg(chat_id, msg)
        elif re_msg.caption_html:
            sent_msg = await Message.send_img(chat_id, re_msg.photo[-1].file_id, msg)
    
    if not sent_msg:
        msg = "An error occurred!"
    else:
        if sent_msg == Forbidden:
            msg =  f"Forbidden!"
        else:
            msg = "Message Sent!"

    await Message.reply_msg(update, msg)
