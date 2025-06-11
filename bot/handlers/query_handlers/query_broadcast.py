import asyncio
from time import time
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest, Forbidden
from bot.utils.database import MemoryDB, MongoDB
from bot.modules.utils import Utils
from bot.helpers import BuildKeyboard

async def query_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("broadcast_")

    # accessing Database
    broadcastData = MemoryDB.data_center.get("broadcast")
    if not broadcastData:
        await query.answer("Session Expired!", True)
        return
    
    # handling query
    if query_data == "none":
        await query.answer()
        return
    
    # only for boolean (toggle)
    elif query_data.startswith("value_"):
        data = query_data.removeprefix("value_")

        existing_data = broadcastData.get(data) # Boolean
        if existing_data:
            broadcastData.update({data: False})
        else:
            broadcastData.update({data: True})
        
        await query.answer(f"Updated: {data}: {broadcastData.get(data)}", True)
    
    elif query_data == "send":
        # variables
        broadcastText = broadcastData["broadcastText"] # only if the message doesn't contain any video/doc or other things
        broadcastCaption = broadcastData["broadcastCaption"] # message with video/audio/doc etc.

        broadcastPhoto = broadcastData["broadcastPhoto"]

        broadcastDocument = broadcastData["broadcastDocument"]
        broadcastDocument_filename = broadcastData["broadcastDocument_filename"]

        broadcastVideo = broadcastData["broadcastVideo"]
        broadcastVideo_note = broadcastData["broadcastVideo_note"]

        broadcastAudio = broadcastData["broadcastAudio"]
        broadcastAudio_filename = broadcastData["broadcastAudio_filename"]

        broadcastVoice = broadcastData["broadcastVoice"]

        is_forward = broadcastData["forward"]
        is_pin = broadcastData["pin"]

        # getting userID from DB
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

        broadcastButton = BuildKeyboard.cbutton([{"Cancel": "broadcast_cancel"}])
        
        try:
            await query.edit_message_text(text, reply_markup=broadcastButton)
        except BadRequest:
            await query.edit_message_caption(text, reply_markup=broadcastData)
        except Exception as e:
            await chat.send_message(str(e))
            return

        broadcastStartTime = time()

        for user_id in active_users:
            sent_message = None

            is_cancelled = broadcastData["is_cancelled"]
            if is_cancelled:
                return
            
            try:
                if is_forward:
                    sent_message = await context.bot.forward_message(user_id, chat.id, broadcastData["replied_message_id"])
                else:
                    if broadcastText:
                        sent_message = await context.bot.send_message(chat_id=user_id, text=broadcastText)
                    elif broadcastPhoto:
                        sent_message = await context.bot.send_photo(chat_id=user_id, photo=broadcastPhoto, caption=broadcastCaption)
                    elif broadcastDocument:
                        sent_message = await context.bot.send_document(chat_id=user_id, document=broadcastDocument, caption=broadcastCaption, filename=broadcastDocument_filename)
                    elif broadcastVideo:
                        sent_message = await context.bot.send_video(chat_id=user_id, video=broadcastVideo, caption=broadcastCaption)
                    elif broadcastVideo_note:
                        sent_message = await context.bot.send_video_note(chat_id=user_id, video_note=broadcastVideo_note)
                    elif broadcastAudio:
                        sent_message = await context.bot.send_audio(chat_id=user_id, audio=broadcastAudio, title=broadcastAudio_filename, caption=broadcastCaption, filename=broadcastAudio_filename)
                    elif broadcastVoice:
                        sent_message = await context.bot.send_voice(chat_id=user_id, voice=broadcastVoice, caption=broadcastCaption)
                
                if sent_message: sent_count += 1

            except Forbidden:
                exception_count += 1
                exception_users_id.append(f"Forbidden: {user_id}")
                # updating MongoDB
                MongoDB.update("users_data", "user_id", int(user_id), "active_status", False)
            
            except Exception as e:
                exception_count += 1
                exception_users_id.append(f"{str(e)}: {user_id}")
            
            if is_pin and sent_message:
                try:
                    await sent_message.pin()
                except:
                    pass
            
            progress = (sent_count + exception_count) * 100 / len(active_users)
            progressBar = Utils.createProgressBar(progress)

            updateText = broadcastUpdateText.format(
                len(users_id),
                len(active_users),
                sent_count,
                exception_count,
                f"{progress:.2f}",
                progressBar
            )

            btn = None if (sent_count + exception_count) == len(active_status) else broadcastButton

            try:
                await query.edit_message_text(updateText, reply_markup=btn)
            except BadRequest:
                await query.edit_message_caption(updateText, reply_markup=btn)
            except Exception as e:
                await chat.send_message(f"An error occured (broadcast still running): {e}")

            await asyncio.sleep(0.5) # sleep for 0.5 sec
        
        broadcastEndTime = time()

        if (broadcastEndTime - broadcastStartTime) > 60:
            time_took = f"{((broadcastEndTime - broadcastStartTime) / 60):.2f} min"
        else:
            time_took = f"{(broadcastEndTime - broadcastStartTime):.2f} sec"
        
        updateText += f"\n\n<b>Broadcast Done ✅: {time_took}</b>"
        
        try:
            await query.edit_message_text(updateText)
        except BadRequest:
            await query.edit_message_caption(updateText)
        except Exception as e:
            await chat.send_message(f"An error occured (After broadcast done): {e}")

        if exception_users_id:
            exception_file = BytesIO(", ".join(exception_users_id).encode())
            exception_file.name = "Exception.txt"

            await chat.send_document(exception_file, f"Total Exception: {len(exception_users_id)}")
    
    elif query_data == "cancel":
        broadcastData.update({"is_cancelled": True})
        await query.answer("Broadcast Cancelled!", True)
