import asyncio
from time import time
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import Forbidden
from ... import logger
from ...helper.button_maker import ButtonMaker
from ...modules.database import MemoryDB, MongoDB
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
        await context.bot.delete_messages(chat.id, [effective_message.id, sent_message.id])
        return
    
    if not re_msg:
        await effective_message.reply_text("Reply a message to broadcast!")
        return

    text = (
        "<blockquote><b>Broadcast</b></blockquote>\n\n"

        "Forward Message: <code>{}</code>\n"
        "Pin Message: <code>{}</code>"
    )

    btn_data = [
        {"Forward Message?": "misc_none", "YES": "misc_broadcast_forward_true", "NO": "misc_broadcast_forward_false"},
        {"Pin Message?": "misc_none", "YES": "misc_broadcast_pin_true", "NO": "misc_broadcast_pin_false"},
        {"Done": "misc_broadcast_done", "Cancel": "misc_broadcast_cancel"}
    ]

    btn = ButtonMaker.cbutton(btn_data)

    # storing required data in datacenter
    data = {
        "broadcast": {
            "text": text,
            "btn": btn,
            "is_forward": False,
            "is_pin": False,
            "is_done": False,
            "is_cancelled": False
        }
    }

    MemoryDB.insert("data_center", user.id, data)

    # accessing datacenter broadcast_data
    broadcast_data = MemoryDB.data_center[user.id]["broadcast"]

    # formatting message
    text = text.format(
        broadcast_data.get("is_forward") or False,
        broadcast_data.get("is_pin") or False
    )
    
    sent_message = await effective_message.reply_text(text, reply_markup=btn)

    for i in range(30):
        await asyncio.sleep(1)
        data_center = MemoryDB.data_center.get(user.id)
        is_done = data_center["broadcast"]["is_done"]
        is_cancelled = data_center["broadcast"]["is_cancelled"]

        if is_done:
            break

        elif is_cancelled:
            await context.bot.edit_message_text("<blockquote><b>Broadcast cancelled!</b></blockquote>", chat.id, sent_message.id)
            return
    
    if not is_done:
        await context.bot.edit_message_text("Oops, Timeout!", chat.id, sent_message.id)
        return
    
    await context.bot.delete_message(chat.id, sent_message.id)
    
    is_forward = data_center["broadcast"]["is_forward"]
    is_pin = data_center["broadcast"]["is_pin"]

    users_id = MongoDB.find("users", "user_id")
    active_status = MongoDB.find("users", "active_status")

    if len(users_id) == len(active_status):
        combined_list = list(zip(users_id, active_status))
        active_users = []
        for active_user_id, is_active in combined_list:
            if is_active == True:
                active_users.append(active_user_id)

    else:
        logger.error(f"Error: UserID {len(users_id)} and ActiveStatus {len(active_status)} aren't equal.")
        active_users = users_id
    
    sent_count, except_count, pin_except_count = 0, 0, 0
    exception_user_ids = []

    notify_btn = ButtonMaker.cbutton([{"Cancel": "misc_broadcast_cancel"}])
    notify_message = await effective_message.reply_text(f"Total users: {len(users_id)}\nActive users: {len(active_users)}", reply_markup=notify_btn)

    start_time = time()

    for user_id in active_users:
        sent_message = None
        is_cancelled = data_center["broadcast"]["is_cancelled"]

        if is_cancelled:
            text = (
                "<blockquote><b>Broadcast Cancelled</b></blockquote>\n\n"
                f"{notify_message.text_html}"
            )

            await context.bot.edit_message_text(text, chat.id, notify_message.id)
            return
        
        try:
            if is_forward:
                sent_message = await context.bot.forward_message(user_id, chat.id, re_msg.id)

            else:
                text = re_msg.text_html
                caption = re_msg.caption_html
                photo = re_msg.photo
                audio = re_msg.audio
                video = re_msg.video
                document = re_msg.document
                voice = re_msg.voice
                video_note = re_msg.video_note

                if text:
                    sent_message = await context.bot.send_message(user_id, text)

                elif photo:
                    sent_message = await context.bot.send_photo(user_id, photo[-1].file_id, caption)

                elif audio:
                    sent_message = await context.bot.send_audio(user_id, audio.file_id, title=audio.file_name, caption=caption, filename=audio.file_name)

                elif video:
                    sent_message = await context.bot.send_video(user_id, video.file_id, caption=caption)

                elif document:
                    sent_message = await context.bot.send_document(user_id, document.file_id, caption, filename=document.file_name)
                
                elif voice:
                    sent_message = await context.bot.send_voice(user_id, voice.file_id, caption=caption)
                
                elif video_note:
                    sent_message = await context.bot.send_video_note(user_id, video_note.file_id)
                
                else:
                    await effective_message.reply_text("Replied content isn't added yet. Stay tuned for future update.")
                    return
            
            if sent_message:
                sent_count += 1

        except Forbidden:
            except_count += 1
            exception_user_ids.append(f"Forbidden: {user_id}")
            MongoDB.update("users", "user_id", int(user_id), "active_status", False)
        
        except Exception as e:
            except_count += 1
            exception_user_ids.append(f"{str(e)}: {user_id}")
        
        if is_pin and sent_message:
            try:
                await context.bot.pin_chat_message(user_id, sent_message.id)
            except Exception as e:
                pin_except_count += 1
                logger.error(e)

        progress = (sent_count + except_count) * 100 / len(active_users)

        updated_text = (
            f"<b>Total users:</b> <code>{len(users_id)}</code>\n"
            f"<b>Active users:</b> <code>{len(active_users)}</code>\n"
            f"<b>Sent:</b> <code>{sent_count}</code>\n"
            f"<b>Exception occurred:</b> <code>{except_count}</code>\n"
            f"<b>Pin exception:</b> <code>{pin_except_count}</code>\n"
            f"<b>Progress:</b> <code>{(progress):.2f}%</code>"
        )
        # cancel btn will be removed if broadcast done
        btn = None if (sent_count + except_count) == len(active_users) else notify_btn
        # update notify message
        notify_message = await context.bot.edit_message_text(updated_text, chat.id, notify_message.id, reply_markup=btn)
        await asyncio.sleep(0.5) # sleep for 0.5 sec
    
    end_time = time()
    if (end_time - start_time) > 60:
        time_took = f"{((end_time - start_time) / 60):.2f} min"
    else:
        time_took = f"{(end_time - start_time):.2f} sec"
    
    
    text = (
        f"<blockquote><b>Broadcast Done</b> [<code>{time_took}</code>]</blockquote>\n\n"
        f"{notify_message.text_html}"
    )

    await context.bot.edit_message_text(text, chat.id, notify_message.id)

    if exception_user_ids:
        exception_file = BytesIO(", ".join(exception_user_ids).encode())
        exception_file.name = "Exception.txt"

        await context.bot.send_document(chat.id, exception_file, f"Total Exception: {len(exception_user_ids)}")
