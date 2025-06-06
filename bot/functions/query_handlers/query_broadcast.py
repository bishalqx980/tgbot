import asyncio
from time import time
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest, Forbidden
from bot.modules.database import MemoryDB, MongoDB
from bot.modules.utils import Utils
from bot.helper import BuildKeyboard
from ..owner_func.broadcast import BroadcastMenu

async def query_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("broadcast_")
    # accessing Database
    chat_data = MemoryDB.data_center.get(chat.id)
    broadcast_data = chat_data.get("broadcast") if chat_data else None
    if not broadcast_data:
        await query.answer("Session Expired!", True)
        return
    
    # handling query
    if query_data == "none":
        await query.answer()
        return
    
    elif query_data == "menu":
        text = BroadcastMenu.TEXT.format(
            "Available" if broadcast_data["media"] else "Not available",
            "Available" if broadcast_data["text"] else "Not available",
            broadcast_data["pin"]
        )
        
        btn = BuildKeyboard.cbutton(BroadcastMenu.BUTTONS)

        try:
            await query.edit_message_text(text, reply_markup=btn)
        except BadRequest:
            await query.delete_message()
            await chat.send_message(text, reply_markup=btn)
        except:
            pass
    
    elif query_data.startswith("add_"):
        # Starting Editing Mode
        MemoryDB.insert("data_center", chat.id, {"photo_file_id": None, "broadcast_text": None, "is_editing": True})

        btn = BuildKeyboard.cbutton([{"Cancel": "broadcast_cancel_editing"}])
        sent_message = await chat.send_message("Now send...", reply_markup=btn)

        for i in range(10):
            data_center = MemoryDB.data_center[chat.id]
            # to check > is operation cancelled
            is_editing = data_center.get("is_editing")
            if not is_editing:
                await query.answer()
                return
            
            await asyncio.sleep(1)
            photo_file_id = data_center.get("photo_file_id")
            broadcast_text = data_center.get("broadcast_text")
            if photo_file_id or broadcast_text:
                break
        
        try:
            message_ids = [sent_message.id]
            if data_center.get("message_id"):
                message_ids.append(data_center.get("message_id"))
            
            await chat.delete_messages(message_ids)
        except:
            pass

        # terminating editing mode
        MemoryDB.insert("data_center", chat.id, {"is_editing": False})

        if not photo_file_id and not broadcast_text:
            await query.answer("Timeout.", True)
            return
        # Updateing broadcast data
        if photo_file_id:
            broadcast_data.update({"media": photo_file_id})
        elif broadcast_text:
            broadcast_data.update({"text": broadcast_text})
        
        await query.answer("Updated...")

        text = BroadcastMenu.TEXT.format(
            "Available" if broadcast_data["media"] else "Not available",
            "Available" if broadcast_data["text"] else "Not available",
            broadcast_data["pin"]
        )
        
        btn = BuildKeyboard.cbutton(BroadcastMenu.BUTTONS)

        try:
            await query.edit_message_text(text, reply_markup=btn)
        except:
            pass
    
    elif query_data == "cancel_editing":
        MemoryDB.insert("data_center", chat.id, {"photo_file_id": None, "broadcast_text": None, "update_data_value": None, "is_editing": False})
        await query.answer("Operation cancelled.", True)
        await query.delete_message()
    
    # only for pin (toggle)
    elif query_data.startswith("value_"):
        data = query_data.removeprefix("value_")

        existing_data = broadcast_data.get(data) # Boolean
        if existing_data:
            broadcast_data.update({data: False})
        else:
            broadcast_data.update({data: True})
        
        await query.answer("Updated...")

        text = BroadcastMenu.TEXT.format(
            "Available" if broadcast_data["media"] else "Not available",
            "Available" if broadcast_data["text"] else "Not available",
            broadcast_data["pin"]
        )
        
        btn = BuildKeyboard.cbutton(BroadcastMenu.BUTTONS)

        try:
            await query.edit_message_text(text, reply_markup=btn)
        except:
            pass
    
    # This is to see all kind of things media/text/btn
    elif query_data.startswith("see_"):
        data = query_data.removeprefix("see_")

        memData = broadcast_data.get(data)
        if not memData:
            await query.answer("No data to show!", True)
            return
        
        btn = BuildKeyboard.cbutton([{"Back": "broadcast_menu"}])

        if data == "media":
            await query.delete_message()
            await chat.send_photo(memData, reply_markup=btn)
        
        else:
            text = (
                "<blockquote><b>Broadcast</b></blockquote>\n\n"
                f"⌈\n{memData}\n⌊"
            )

            await query.edit_message_text(text, reply_markup=btn)
    
    elif query_data == "preview":
        media = broadcast_data["media"]
        text = broadcast_data["text"]
        pin_message = broadcast_data["pin"]

        if not media and not text:
            await query.answer("No data to show!", True)
            return
        else:
            await query.answer()

        if media:
            sent_message = await chat.send_photo(media, text)
        else:
            sent_message = await chat.send_message(text)
        
        if pin_message:
            await sent_message.pin()
    
    elif query_data == "sendToAll":
        broadcastMedia = broadcast_data["media"]
        broadcastText = broadcast_data["text"]
        pin_message = broadcast_data["pin"]

        if not broadcastMedia and not broadcastText:
            await query.answer("Media or Text isn't given!", True)
            return
        
        users_id = MongoDB.find("users_data", "user_id")
        active_status = MongoDB.find("users_data", "active_status")
        active_users = []

        if len(users_id) != len(active_status):
            active_users = users_id
        else:
            combined_list = list(zip(users_id, active_status))
            for user_id, is_active in combined_list:
                if is_active: active_users.append(user_id)
        
        # counters
        sent_count = 0
        exception_count = 0
        progress = 0
        # exception happend with users ID
        exception_users_id = []

        broadcastUpdateText = (
            "<blockquote><b>Broadcast</b></blockquote>\n\n"

            "<b>📦 Database information</b>\n"
            "<b>• Total users:</b> <code>{}</code>\n"
            "<b>• Active users:</b> <code>{}</code>\n\n"

            "<b>📊 Progress</b>\n"
            "<b>• Sent:</b> <code>{}</code>\n"
            "<b>• Exception:</b> <code>{}</code>\n"
            "<b>• Progress:</b> <code>{}%</code>\n"
            "{}" # progress bar
        )

        text = broadcastUpdateText.format(
            len(users_id),
            len(active_users),
            sent_count,
            exception_count,
            f"{progress:.2f}",
            "[]"
        )

        broadcastBtn = BuildKeyboard.cbutton([{"Cancel": "broadcast_cancel"}])
        await query.edit_message_text(text, reply_markup=broadcastBtn)

        broadcastStartTime = time()

        for user_id in active_users:
            sent_message = None

            is_cancelled = broadcast_data["is_cancelled"]
            if is_cancelled:
                return
            
            try:
                if broadcastMedia:
                    sent_message = await context.bot.send_photo(user_id, broadcastMedia, broadcastText)
                else:
                    sent_message = await context.bot.send_message(user_id, broadcastText)
                
                if sent_message: sent_count += 1

            except Forbidden:
                exception_count += 1
                exception_users_id.append(f"Forbidden: {user_id}")
                # updating MongoDB
                MongoDB.update("users_data", "user_id", int(user_id), "active_status", False)
            
            except Exception as e:
                exception_count += 1
                exception_users_id.append(f"{str(e)}: {user_id}")
            
            if pin_message and sent_message:
                try:
                    await sent_message.pin()
                except:
                    pass
            
            progress = (sent_count + exception_count) * 100 / len(active_users)
            progressBar = Utils.createProgressBar(progress)

            text = broadcastUpdateText.format(
                len(users_id),
                len(active_users),
                sent_count,
                exception_count,
                f"{progress:.2f}",
                progressBar
            )

            btn = None if (sent_count + exception_count) == len(active_status) else broadcastBtn

            try:
                await query.edit_message_text(text, reply_markup=btn)
            except:
                pass

            await asyncio.sleep(0.5) # sleep for 0.5 sec
        
        broadcastEndTime = time()

        if (broadcastEndTime - broadcastStartTime) > 60:
            time_took = f"{((broadcastEndTime - broadcastStartTime) / 60):.2f} min"
        else:
            time_took = f"{(broadcastEndTime - broadcastStartTime):.2f} sec"
        
        text += f"\n\n<b>Broadcast Done ✅: {time_took}</b>"
        await query.edit_message_text(text)

        if exception_users_id:
            exception_file = BytesIO(", ".join(exception_users_id).encode())
            exception_file.name = "Exception.txt"

            await chat.send_document(exception_file, f"Total Exception: {len(exception_users_id)}")
    
    elif query_data == "cancel":
        broadcast_data.update({"is_cancelled": True})
        await query.answer("Broadcast Cancelled!", True)
    
    elif query_data == "close":
        try:
            message_id = query.message.message_id
            await chat.delete_messages([message_id, message_id - 1])
        except:
            try:
                await query.delete_message()
            except:
                pass
