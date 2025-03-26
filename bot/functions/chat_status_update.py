from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.modules.database.common import database_search
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins

async def chat_status_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    **Status updates of `effective_chat` >> Group/SuperGroup**
    """
    chat = update.effective_chat
    cause_user = update.effective_user
    effective_message = update.effective_message

    response, database_data = database_search("groups", "chat_id", chat.id)
    if response == False:
        return

    welcome_user = database_data.get("welcome_user")
    custom_welcome_msg = database_data.get("custom_welcome_msg")
    farewell_user = database_data.get("farewell_user")
    antibot = database_data.get("antibot")

    # handling new chat member
    if effective_message.new_chat_members:
        victim = effective_message.new_chat_members

        # Antibot
        if victim.is_bot and antibot:
            chat_admins = await fetch_chat_admins(chat, context.bot.id, cause_user.id)

            if chat_admins["is_user_owner"]:
                return
            
            elif chat_admins["is_user_admin"] and (chat_admins["is_user_admin"].can_invite_users or chat_admins["is_user_admin"].can_promote_members):
                return
            
            if not chat_admins["is_bot_admin"]:
                await context.bot.send_message(chat.id, "Antibot Error: I'm not an admin in this chat!")
                return
            
            if not chat_admins["is_bot_admin"].can_restrict_members:
                await context.bot.send_message(chat.id, "Antibot Error: I don't have enough permission to restrict chat members!")
                return
            
            try:
                await chat.unban_member(victim.id)
            except Exception as e:
                logger.error(e)
                await context.bot.send_message(chat.id, str(e))
                return
            
            await context.bot.send_message(chat.id, f"Antibot: {victim.mention_html()} has been kicked from this chat!")
        
        # greeting new chat member
        elif welcome_user:
            if custom_welcome_msg:
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
                    greeting_message = custom_welcome_msg.replace(key, str(value) if value else "")
            
            else:
                greeting_message = f"Hi, {victim.mention_html()}! Welcome to {chat.title}!"

            await context.bot.send_message(chat.id, greeting_message)
    
    # farewell for left chat member
    elif effective_message.left_chat_member and farewell_user:
        await context.bot.send_message(chat.id, f"Nice to see you! {effective_message.left_chat_member.mention_html()} has left us!")
    




