from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.modules.database.common import database_search
from bot.functions.group_management.auxiliary.chat_member_status import chat_member_status
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins

async def chat_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    effective_message = update.effective_message
    chat_member = update.chat_member
    cause_user = chat_member.from_user
    victim = chat_member.new_chat_member.user

    response, database_data = database_search("groups", "chat_id", chat.id)
    if response == False:
        # await effective_message.reply_text(database_data)
        return

    welcome_user = database_data.get("welcome_user")
    custom_welcome_msg = database_data.get("custom_welcome_msg")
    farewell_user = database_data.get("farewell_user")
    antibot = database_data.get("antibot")

    member_status = chat_member_status(chat_member) #True means user exist and False is not exist
    if not member_status:
        return
    
    is_user_exist, cause = member_status

    if is_user_exist and cause == "JOINED":
        if victim.is_bot and antibot:
            chat_admins = await fetch_chat_admins(chat, context.bot.id, cause_user.id, victim.id)

            if chat_admins["is_user_owner"]:
                return
            
            elif chat_admins["is_user_admin"] and chat_admins["is_user_admin"].can_invite_users:
                return

            if chat_admins["is_victim_admin"]:
                await effective_message.reply_text(f"Antibot error: {victim.mention_html()} has been added as an admin!")
                return
            
            if not chat_admins["is_bot_admin"]:
                await effective_message.reply_text("I'm not an admin in this chat!")
                return
            
            if not chat_admins["is_bot_admin"].can_restrict_members:
                await effective_message.reply_text("I don't have enough permission to restrict chat members!")
                return
            
            try:
                await chat.unban_member(victim.id)
            except Exception as e:
                logger.error(e)
                await effective_message.reply_text(str(e))
                return
            
            await effective_message.reply_text(f"Antibot: {victim.mention_html()} has been kicked from this chat!")
        
        elif welcome_user:
            if not custom_welcome_msg:
                await effective_message.reply_text(f"Hi, {victim.mention_html()}! Welcome to {chat.title}!")

            else:
                formattings = {
                    "{first}": victim.first_name,
                    "{last}": victim.last_name,
                    "{fullname}": victim.full_name,
                    "{username}": victim.username,
                    "{mention}": victim.mention_html(),
                    "{id}": victim.id,
                    "{chatname}": chat.title
                }

                for key, value in formattings.items():
                    if not value:
                        value = ""
                    custom_welcome_msg = custom_welcome_msg.replace(key, str(value))

                await effective_message.reply_text(custom_welcome_msg)

    elif not is_user_exist and cause == "LEFT" and farewell_user:
        await effective_message.reply_text(f"Nice to see you! {victim.mention_html()} has left us!")
