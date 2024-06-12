import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.modules.safone import Safone


async def func_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    prompt = " ".join(context.args)

    if chat.type != "private":
        find_group = await LOCAL_DATABASE.find_one("groups", chat.id)
        if not find_group:
            find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
            if find_group:
                await LOCAL_DATABASE.insert_data("groups", chat.id, find_group)
            else:
                await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
                return
        
        ai_status = find_group.get("ai_status")
        if not ai_status and ai_status != None:
            await Message.del_msg(chat.id, e_msg)
            return

    if not prompt:
        await Message.reply_msg(update, "Use <code>/imagine prompt</code>\nE.g. <code>/imagine a cute cat</code>")
        return
    
    sent_msg = await Message.reply_msg(update, "Processing...")
    retry, attempt = 0, 2
    while retry != attempt:
        imagine = await Safone.imagine(prompt)
        if imagine:
            break
        elif retry == attempt:
            await Message.edit_msg(update, "Too many requests! Please try after sometime!", sent_msg)
            return
        retry += 1
        await Message.edit_msg(update, f"Please wait, Imagine is busy!\nAttempt: {retry}/{attempt}", sent_msg)
        await asyncio.sleep(3)
    
    await Message.del_msg(chat.id, sent_msg)
    
    msg = f"» <i>{prompt}</i>"
    if chat.type != "private":
        msg += f"\n<b>Req by</b>: {user.mention_html()}"
    
    await Message.send_img(chat.id, imagine, msg)
