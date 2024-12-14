import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from bot.helper.telegram_helper import Message
from bot.modules.database.combined_db import global_search
# from bot.modules.unused.g4f import G4F


async def func_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await Message.reply_msg(update, "This function has been disabled for some limitations! Stay tuned for further notice.")
    return

    '''
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message
    prompt = " ".join(context.args)

    if chat.type != "private":
        db = await global_search("groups", "chat_id", chat.id)
        if db[0] == False:
            await Message.reply_msg(update, db[1])
            return
        
        find_group = db[1]
        
        ai_status = find_group.get("ai_status") or True
        if not ai_status:
            await Message.del_msg(chat.id, e_msg)
            return
    
    if not prompt:
        await Message.reply_msg(update, "Use <code>/gpt your_prompt</code>\nE.g. <code>/gpt what can you do?</code>")
        return
    
    common_words = ["hi", "hello"]
    if prompt.lower() in common_words:
        await Message.reply_msg(update, "Hello! How can I assist you today?")
        return
    
    sent_msg = await Message.reply_msg(update, "Processing...")
    retry, attempt = 0, 3
    while retry != attempt:
        g4f_gpt = await G4F.chatgpt(f"{prompt}, explain in few sentences and in English.")
        if g4f_gpt:
            break
        elif retry == attempt:
            await Message.edit_msg(update, "Too many requests! Please try after sometime!", sent_msg)
            return
        retry += 1
        await Message.edit_msg(update, f"Please wait, ChatGPT is busy!\nAttempt: {retry}/{attempt}", sent_msg)
        await asyncio.sleep(3)
    
    if chat.type != "private":
        g4f_gpt += f"\n\n*Req by*: {user.mention_markdown()}"
    
    await Message.edit_msg(update, g4f_gpt, sent_msg, parse_mode=ParseMode.MARKDOWN)
    '''
