async def func_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    replied_msg = update.message.reply_to_message
    inline_text = " ".join(context.args)

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "❗ This command is only for bot owner!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, "⚠ Boss you are in public!")
        return
    
    msg = replied_msg.text_html or replied_msg.caption_html if replied_msg else None

    if not replied_msg:
        await Message.reply_msg(update, "Reply a message to broadcast!\n<code>/broadcast f</code> to forwared message!")
        return
    
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
        try: 
            user_id = to_whom
            if forward_confirm:
                await Message.forward_msg(user_id, chat.id, replied_msg.id)
            else:
                if msg:
                    if replied_msg.text_html:
                        await Message.send_msg(user_id, msg)
                    elif replied_msg.caption:
                        await Message.send_img(user_id, replied_msg.photo[-1].file_id, msg)
                else:
                    await Message.reply_msg(update, "Message to broadcast, not found!")
                    return
            await Message.reply_msg(update, "<i>Message Sent...!</i>")
        except Exception as e:
            logger.error(e)
            await Message.reply_msg(update, f"Error Broadcast: {e}")
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
                await Message.forward_msg(user_id, chat.id, replied_msg.id)
            else:
                if msg:
                    if replied_msg.text_html:
                        await Message.send_msg(user_id, msg)
                    elif replied_msg.caption:
                        await Message.send_img(user_id, replied_msg.photo[-1].file_id, msg)
                else:
                    await Message.reply_msg(update, "Message to broadcast, not found!")
                    await Message.del_msg(chat.id, notify)
                    return
            sent_count += 1
            progress = (sent_count + except_count) * 100 / len(active_users)
            await Message.edit_msg(update, f"Total Users: {len(users_id)}\nActive Users: {len(active_users)}\nSent: {sent_count}\nException occurred: {except_count}\nProgress: {int(progress)}%", notify)
            # sleep for 0.5sec
            await asyncio.sleep(0.5)
        except Exception as e:
            except_count += 1
            logger.error(e)
    end_time = time.time()
    await Message.reply_msg(update, f"<i>Broadcast Done...!\nTime took: {(end_time - start_time):.2f}</i>")