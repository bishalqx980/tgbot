import asyncio
from time import time
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import Forbidden
from bot import logger



from bot.modules.database import MemoryDB, MongoDB
from bot.functions.sudo_users import fetch_sudos


async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    re_msg = effective_message.reply_to_message

    power_users = fetch_sudos()
    if user.id not in power_users:
        await effective_message.reply_text("Access denied!")
        return
    
    if chat.type != ChatType.PRIVATE:
        await effective_message.reply_text(f"This command is made to be used in pm, not in public chat!")
        await asyncio.sleep(3)
        await Message.delete_messages(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    if not re_msg:
        await effective_message.reply_text("Reply a message to broadcast!")
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
            "is_forward": False,
            "is_pin": False,
            "is_done": False
        }
    }

    MemoryDB.insert_data("data_center", user.id, data)

    data_center = MemoryDB.data_center.get(user.id)
    db_broadcast = data_center.get("broadcast")
    is_forward = db_broadcast.get("is_forward", False)
    is_pin = db_broadcast.get("is_pin", False)
    
    msg = (
        "<b><u>Broadcast</u></b>\n\n"
        f"Forward: <code>{is_forward}</code>\n"
        f"Pin message: <code>{is_pin}</code>"
    )

    btn_data = [
        {"Forward?": "query_none", "YES": "query_broadcast_forward_true", "NO": "query_broadcast_forward_false"},
        {"Pin message?": "query_none", "YES": "query_broadcast_pin_true", "NO": "query_broadcast_pin_false"},
        {"Done": "query_broadcast_done", "Close": "query_close"}
    ]

    btn = ButtonMaker.cbutton(btn_data)
    sent_msg = await effective_message.reply_text(msg, reply_markup=btn)

    timeout = 0
    while timeout < 30:
        timeout += 1
        await asyncio.sleep(1)
        data_center = MemoryDB.data_center.get(user.id)
        is_done = data_center["broadcast"]["is_done"]
        if is_done:
            break
    
    await Message.delete_message(chat.id, sent_msg)

    if not is_done:
        await effective_message.reply_text("Oops, Timeout!")
        return
    
    is_forward = data_center["broadcast"]["is_forward"]
    is_pin = data_center["broadcast"]["is_pin"]
    
    broadcast_msg = re_msg.text_html or re_msg.caption_html

    users_id = MongoDB.find("users", "user_id")
    active_status = MongoDB.find("users", "active_status")

    if len(users_id) == len(active_status):
        combined_list = list(zip(users_id, active_status))
        active_users = []
        for filter_user_id in combined_list:
            if filter_user_id[1] == True:
                active_users.append(filter_user_id[0])
    else:
        await effective_message.reply_text(f"An error occured!\nuser_id: {len(user_id)} isn't equal to active_status: {len(active_status)} !!")
        return
    
    sent_count, except_count, pin_except_count = 0, 0, 0
    exception_user_ids = []
    notify_btn = ButtonMaker.cbutton([{"Cancel": "query_close"}])
    notify = await Message.send_message(user.id, f"Total users: {len(users_id)}\nActive users: {len(active_users)}", btn=notify_btn)
    start_time = time()

    for user_id in active_users:
        if is_forward:
            sent_msg = await Message.forward_message(user_id, chat.id, re_msg.id)
        else:
            if re_msg.text_html:
                sent_msg = await Message.send_message(user_id, broadcast_msg)
            elif re_msg.caption_html:
                sent_msg = await Message.send_image(user_id, re_msg.photo[-1].file_id, broadcast_msg)
        
        if not sent_msg:
            except_count += 1
            exception_user_ids.append(f"🤷‍♂: <code>{user_id}</code>")
        elif sent_msg == Forbidden:
            except_count += 1
            exception_user_ids.append(f"Forbidden: <code>{user_id}</code>")
            MongoDB.update_db("users", "user_id", int(user_id), "active_status", False)
        else:
            sent_count += 1
            if is_pin:
                try:
                    await bot.pin_chat_message(user_id, sent_msg.id)
                except Exception as e:
                    pin_except_count += 1
                    logger.error(e)

        progress = (sent_count + except_count) * 100 / len(active_users)
        edit_msg = (
            f"<b>Total users:</b> <code>{len(users_id)}</code>\n"
            f"<b>Active users:</b> <code>{len(active_users)}</code>\n"
            f"<b>Sent:</b> <code>{sent_count}</code>\n"
            f"<b>Exception occurred:</b> <code>{except_count}</code>\n"
            f"<b>Pin exception:</b> <code>{pin_except_count}</code>\n"
            f"<b>Progress:</b> <code>{(progress):.2f}%</code>"
        )
        edit_msg_btn = None if (sent_count + except_count) == len(active_users) else notify_btn
        edited_msg = await Message.edit_message(update, edit_msg, notify, edit_msg_btn)
        if edited_msg:
            await asyncio.sleep(0.5) # sleep for 0.5 sec
        else:
            msg = (
                "<b>⚠️ Operation cancelled!</b>\n\n"
                "<b>» Progress</b>\n"
                f"{edit_msg}"
            )
            await effective_message.reply_text(msg)
            break

    end_time = time()
    time_took = f"{(end_time - start_time):.2f} sec"
    if (end_time - start_time) > 60:
        time_took = f"{((end_time - start_time) / 60):.2f} min"
    
    msg = f"✅ Broadcast Done!\nTime took: <code>{time_took}</code>"
    if len(exception_user_ids) > 0:
        msg += f"\nException user ids: {exception_user_ids}"
    
    await effective_message.reply_text(f"<b>{msg}</b>")
