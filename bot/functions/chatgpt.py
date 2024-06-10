async def func_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await Message.reply_msg(update, "Use <code>/gpt your_prompt</code>\nE.g. <code>/gpt What is AI?</code>")
        return
    
    common_words = ["hi", "hello"]
    if prompt.lower() in common_words:
        await Message.reply_msg(update, "Hello! How can I assist you today?")
        return
    
    sent_msg = await Message.reply_msg(update, "Processing...")
    retry = 0

    while retry != 3:
        g4f_gpt = await G4F.chatgpt(f"{prompt}, explain in few sentences and in English.")
        if g4f_gpt and "流量异常, 请尝试更换网络环境, 如果你觉得ip被误封了, 可尝试邮件联系我们, 当前" not in g4f_gpt:
            break
        elif retry == 3:
            await Message.edit_msg(update, "Too many requests! Please try after sometime!", sent_msg)
            return
        retry += 1
        await Message.edit_msg(update, f"Please wait, ChatGPT is busy!\nAttempt: {retry}", sent_msg)
        await asyncio.sleep(3)
    
    try:
        if chat.type != "private":
            g4f_gpt += f"\n\n*Req by*: {user.mention_markdown()}"
        await Message.edit_msg(update, g4f_gpt, sent_msg, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(e)
        await Message.edit_msg(update, f"Error ChatGPT: {e}", sent_msg)