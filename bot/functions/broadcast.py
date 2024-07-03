import time
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import Forbidden
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.database.mongodb import MongoDB
from bot.functions.power_users import _power_users


async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = update.message.reply_to_message
    inline_text = " ".join(context.args)

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
    
    if not re_msg:
        await Message.reply_msg(update, "Reply a message to broadcast!\n<code>/broadcast f</code> to forwared message!")
        return
    
    msg = re_msg.text_html or re_msg.caption_html if re_msg else None

    forward_confirm, to_whom = None, None

    if inline_text:
        inline_text_split = inline_text.split()
        if len(inline_text_split) == 2:
            forward_confirm, to_whom = inline_text_split
        elif len(inline_text_split) == 1:
            if inline_text_split[0] == "f":
                forward_confirm = True
            else:
                to_whom = inline_text_split[0]
    
    if to_whom:
        user_id = to_whom
        if forward_confirm:
            sent_msg = await Message.forward_msg(user_id, chat.id, re_msg.id)
        else:
            if re_msg.text_html:
                sent_msg = await Message.send_msg(user_id, msg)
            elif re_msg.caption:
                sent_msg = await Message.send_img(user_id, re_msg.photo[-1].file_id, msg)
        
        if sent_msg == Forbidden:
            await Message.reply_msg(update, f"Error Broadcast: Forbidden")
        else:
            await Message.reply_msg(update, "<i>Message Sent...!</i>")
        return
    
    users_id = await MongoDB.find("users", "user_id")
    active_status = await MongoDB.find("users", "active_status")

    if len(users_id) == len(active_status):
        combined_list = list(zip(users_id, active_status))
        active_users = []
        for filter_user_id in combined_list:
            if filter_user_id[1] == True:
                active_users.append(filter_user_id[0])
    else:
        await Message.reply_msg(update, f"Error: Users {len(user_id)} not equal to active_status {len(active_status)}...!")
        return

    sent_count, except_count = 0, 0
    notify = await Message.send_msg(user.id, f"Total Users: {len(users_id)}\nActive Users: {len(active_users)}")
    start_time = time.time()
    for user_id in active_users:
        try:
            if forward_confirm:
                sent_msg = await Message.forward_msg(user_id, chat.id, re_msg.id)
            else:
                if re_msg.text_html:
                    sent_msg = await Message.send_msg(user_id, msg)
                elif re_msg.caption:
                    sent_msg = await Message.send_img(user_id, re_msg.photo[-1].file_id, msg)

            if sent_msg:
                sent_count += 1
                progress = (sent_count + except_count) * 100 / len(active_users)
                progress_bar = ("▣" * int(((sent_count + except_count) * 10) / len(active_users))) + ("□" * int(10 - int(((sent_count + except_count) * 10) / len(active_users))))
                await Message.edit_msg(update, f"Total Users: {len(users_id)}\nActive Users: {len(active_users)}\nSent: {sent_count}\nException occurred: {except_count}\nProgress: {int(progress)}%\n» {progress_bar} «", notify)
                # sleep for 0.5sec
                await asyncio.sleep(0.5)
        except Exception as e:
            except_count += 1
            logger.error(e)
    end_time = time.time()
    time_took = f"{(end_time - start_time):.2f} sec"
    if (end_time - start_time) > 60:
        time_took = f"{((end_time - start_time) / 60):.2f} min"
    await Message.reply_msg(update, f"<i>Broadcast Done...!\nTime took: {time_took}</i>")
