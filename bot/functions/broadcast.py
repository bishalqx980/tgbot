import time
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.functions.power_users import _power_users


async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = update.message.reply_to_message

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
        await Message.reply_msg(update, "Reply a message to broadcast!")
        return
    
    data = {
        "user_id": user.id,
        "chat_id": chat.id,
        "collection_name": "data_center",
        "db_find": "user_id",
        "db_vlaue": user.id,
        "edit_data_key": None,
        "edit_data_value": None,
        "del_msg_pointer_id": e_msg.id,
        "edit_data_value_msg_pointer_id": None,
        "broadcast": {
            "is_forward": None,
            "is_pin": None,
            "is_done": None
        }
    }

    await LOCAL_DATABASE.insert_data("data_center", user.id, data)

    localdb = await LOCAL_DATABASE.find_one("data_center", user.id)
    db_broadcast = localdb.get("broadcast")
    is_forward = db_broadcast.get("is_forward") or False
    is_pin = db_broadcast.get("is_pin") or False
    
    msg = (
        "<b><u>Broadcast</u></b>\n\n"
        f"Forward: <code>{is_forward}</code>\n"
        f"Pin message: <code>{is_pin}</code>"
    )

    btn_name_row1 = ["Forward?", "YES", "NO"]
    btn_data_row1 = ["query_none", "query_broadcast_forward_true", "query_broadcast_forward_false"]

    btn_name_row2 = ["Pin message?", "YES", "NO"]
    btn_data_row2 = ["query_none", "query_broadcast_pin_true", "query_broadcast_pin_false"]

    btn_name_row3 = ["Done", "Close"]
    btn_data_row3 = ["query_broadcast_done", "query_close"]

    row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
    row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
    row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

    btn = row1 + row2 + row3

    sent_msg = await Message.reply_msg(update, msg, btn)

    timeout = 0

    while timeout < 30:
        timeout += 1
        await asyncio.sleep(1)
        localdb = await LOCAL_DATABASE.find_one("data_center", user.id)
        db_broadcast = localdb.get("broadcast")
        is_done = db_broadcast.get("is_done")
        if is_done:
            break
    
    await Message.del_msg(chat.id, sent_msg)

    if not is_done:
        await Message.reply_msg(update, "Oops, Timeout!")
        return
    
    is_forward = db_broadcast.get("is_forward")
    is_pin = db_broadcast.get("is_pin")
    
    broadcast_msg = re_msg.text_html or re_msg.caption_html

    users_id = await MongoDB.find("users", "user_id")
    active_status = await MongoDB.find("users", "active_status")

    if len(users_id) == len(active_status):
        combined_list = list(zip(users_id, active_status))
        active_users = []
        for filter_user_id in combined_list:
            if filter_user_id[1] == True:
                active_users.append(filter_user_id[0])
    else:
        await Message.reply_msg(update, f"An error occured!\nuser_id: {len(user_id)} isn't equal to active_status: {len(active_status)} !!")
        return
    
    sent_count, except_count, pin_except_count = 0, 0, 0
    notify = await Message.send_msg(user.id, f"Total users: {len(users_id)}\nActive users: {len(active_users)}")
    start_time = time.time()

    for user_id in active_users:
        if is_forward:
            sent_msg = await Message.forward_msg(user_id, chat.id, re_msg.id)
        else:
            if re_msg.text_html:
                sent_msg = await Message.send_msg(user_id, broadcast_msg)
            elif re_msg.caption_html:
                sent_msg = await Message.send_img(user_id, re_msg.photo[-1].file_id, broadcast_msg)
        
        if not sent_msg:
            except_count += 1
        else:
            sent_count += 1
            if is_pin:
                try:
                    await bot.pin_chat_message(user_id, sent_msg.id)
                except Exception as e:
                    pin_except_count += 1
                    logger.error(e)

        progress = (sent_count + except_count) * 100 / len(active_users)
        await Message.edit_msg(update, f"Total users: {len(users_id)}\nActive users: {len(active_users)}\nSent: {sent_count}\nException occurred: {except_count}\nPin exception: {pin_except_count}\nProgress: {(progress):.2f}%", notify)
        # sleep for 0.5 sec
        await asyncio.sleep(0.5)
    
    end_time = time.time()
    time_took = f"{(end_time - start_time):.2f} sec"
    if (end_time - start_time) > 60:
        time_took = f"{((end_time - start_time) / 60):.2f} min"
    
    await Message.reply_msg(update, f"Broadcast Done!\nTime took: {time_took}")
