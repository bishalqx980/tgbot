from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.modules.group_management.log_channel import _log_channel
from bot.modules.group_management.check_permission import _check_permission
from bot.modules.group_management.chat_member_status import _chat_member_status


async def track_chat_activities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    this will check chat status (if any user joined or left etc.)
    """
    chat = update.effective_chat
    chat_member = update.chat_member

    user = chat_member.from_user # cause user
    victim = chat_member.new_chat_member.user

    find_group = await LOCAL_DATABASE.find_one("groups", chat.id)
    if not find_group:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
        if find_group:
            await LOCAL_DATABASE.insert_data("groups", chat.id, find_group)
        else:
            return

    welcome_msg = find_group.get("welcome_msg")
    custom_welcome_msg = find_group.get("custom_welcome_msg")
    goodbye_msg = find_group.get("goodbye_msg")
    antibot = find_group.get("antibot")

    _chk_stat = await _chat_member_status(chat_member) #True means user exist and False is not exist

    if not _chk_stat:
        return
    
    user_exist, cause = _chk_stat

    await _log_channel(context, chat, user, victim, action=cause)

    if user_exist == True:
        if victim.is_bot and antibot:
            _chk_per = await _check_permission(update, victim, user)

            if not _chk_per:
                return
            
            _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

            if bot_permission.status != ChatMember.ADMINISTRATOR:
                await Message.send_msg(chat.id, "<b>Antibot:</b> I'm not an admin in this chat!")
                return
            
            if not bot_permission.can_restrict_members:
                await Message.reply_msg(update, "I don't have enough rights to restrict/unrestrict chat member!")
                return
            
            if victim_permission.status == ChatMember.ADMINISTRATOR:
                await Message.send_msg(chat.id, f"<b>Antibot:</b> {victim.mention_html()} has been added as an admin. I can't ban an admin!")
                return
            
            try:
                await bot.ban_chat_member(chat.id, victim.id)
                await Message.send_msg(chat.id, f"Antibot has banned {victim.mention_html()} from this chat!")
            except Exception as e:
                logger.error(e)
                await Message.send_msg(chat.id, f"Error: {e}")
        elif welcome_msg:
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

                await Message.send_msg(chat.id, custom_welcome_msg)
            else:
                await Message.send_msg(chat.id, f"Hi, {victim.mention_html()}! Welcome to {chat.title}")
    elif user_exist == False and cause == "LEFT" and goodbye_msg:
        await Message.send_msg(chat.id, f"{victim.mention_html()} just left the chat...")
