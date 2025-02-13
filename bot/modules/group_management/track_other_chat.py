from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.database.combined_db import global_search
from bot.modules.group_management.log_channel import _log_channel
from bot.modules.group_management.check_permission import _check_permission
from bot.modules.group_management.chat_member_status import _chat_member_status


async def track_other_chat_act(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    this will check chat status (if any user joined or left etc.)
    """
    chat = update.effective_chat
    chat_member = update.chat_member

    user = chat_member.from_user # cause user
    victim = chat_member.new_chat_member.user

    db = await global_search("groups", "chat_id", chat.id)
    if db[0] == False:
        # await Message.reply_message(update, db[1])
        return
    
    find_group = db[1]

    welcome_user = find_group.get("welcome_user")
    custom_welcome_msg = find_group.get("custom_welcome_msg")
    farewell_user = find_group.get("farewell_user")
    antibot = find_group.get("antibot")

    _chk_stat = await _chat_member_status(chat_member) #True means user exist and False is not exist

    if not _chk_stat:
        return
    
    user_exist, cause = _chk_stat

    await _log_channel(update, chat, user, victim, action=cause)

    if user_exist == True and cause == "JOINED":
        if victim.is_bot and antibot:
            _chk_per = await _check_permission(update, victim, user)

            if not _chk_per:
                return
            
            _bot_info, bot_permission, user_permission, victim_permission = _chk_per

            if bot_permission.status != ChatMember.ADMINISTRATOR:
                await Message.send_message(chat.id, "<b>Antibot:</b> I'm not an admin in this chat!")
                return
            
            if not bot_permission.can_restrict_members:
                await Message.reply_message(update, "I don't have enough rights to restrict/unrestrict chat member!")
                return
            
            if user_permission.status == ChatMember.ADMINISTRATOR:
                if user_permission.can_invite_users:
                    return
            
            if victim_permission.status == ChatMember.ADMINISTRATOR:
                await Message.send_message(chat.id, f"<b>Antibot:</b> {victim.mention_html()} has been added as an admin. I can't kick an admin!")
                return
            
            try:
                await bot.unban_chat_member(chat.id, victim.id)
                await Message.send_message(chat.id, f"Antibot has kicked {victim.mention_html()} from this chat!")
            except Exception as e:
                logger.error(e)
                await Message.reply_message(update, str(e))
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
                    if not value:
                        value = ""
                    custom_welcome_msg = custom_welcome_msg.replace(key, str(value))

                await Message.send_message(chat.id, custom_welcome_msg)
            else:
                await Message.send_message(chat.id, f"Hi, {victim.mention_html()}! Welcome to {chat.title}")
    elif user_exist == False and cause == "LEFT" and farewell_user:
        await Message.send_message(chat.id, f"{victim.mention_html()} just left the chat...")
