from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.mongodb import MongoDB


async def _check_permission(update: Update, victim=None, user=None, checking_msg=True):
    chat = update.effective_chat

    if checking_msg:
        del_msg = await Message.send_msg(chat.id, "Checking permission...")

    _bot_info = await bot.get_me()
    bot_permission = await chat.get_member(_bot_info.id)

    user_permission = await chat.get_member(user.id) if user else None

    admin_rights = None

    if user_permission.status == ChatMember.ADMINISTRATOR:
        admins = await bot.get_chat_administrators(chat.id)
        for admin in admins:
            if admin.user.id == user.id:
                admin_rights = {
                    "can_change_info": admin.can_change_info,
                    "can_delete_messages": admin.can_delete_messages,
                    "can_invite_users": admin.can_invite_users,
                    "can_pin_messages": admin.can_pin_messages,
                    "can_promote_members": admin.can_promote_members,
                    "can_restrict_members": admin.can_restrict_members,
                    "is_anonymous": admin.is_anonymous
                }
    victim_permission = await chat.get_member(victim.id) if victim else None
    
    if checking_msg:
        try:
            await Message.del_msg(chat.id, del_msg)
        except Exception as e:
            logger.error(f"Error: {e}")

    return _bot_info, bot_permission, user_permission, admin_rights, victim_permission


async def _chat_member_status(c_mem_update: ChatMemberUpdated):
    dif = c_mem_update.difference()
    status = dif.get("status")

    if not status:
        return

    old_status, new_status = status

    was_logic = [ChatMember.LEFT, ChatMember.BANNED] #ChatMember.RESTRICTED
    exist_logic = [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    if old_status in was_logic and new_status in exist_logic:
        user_exist = True
        reason = None
    elif old_status in exist_logic and new_status in was_logic:
        user_exist = False
        if new_status == ChatMember.LEFT:
            reason = "left"
        elif new_status == ChatMember.RESTRICTED:
            reason = "restricted"
        elif new_status == ChatMember.BANNED:
            reason = "banned"
    else:
        user_exist = None
        reason = None
    return user_exist, reason


async def _check_del_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    only delete group chat commands
    """
    chat = update.effective_chat
    msg = update.effective_message

    if chat.type == "private":
        return
    
    try:
        find_group = context.chat_data["db_chat_data"]
    except Exception as e:
        logger.error(f"Error: {e}")

        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
        if find_group:
            context.chat_data["db_chat_data"] = find_group
        else:
            await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
            return

    del_cmd = find_group.get("del_cmd")
    if del_cmd:
        await Message.del_msg(chat.id, msg)


async def _log_channel(context: ContextTypes.DEFAULT_TYPE, chat, user, victim=None, action=None, reason=None):
    """
    sends chat actions to log channel
    """
    try:
        find_group = context.chat_data["db_chat_data"]
    except Exception as e:
        logger.error(f"Error: {e}")

        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
        if find_group:
            context.chat_data["db_chat_data"] = find_group
        else:
            return
    
    log_channel = find_group.get("log_channel")
    if not log_channel:
        return
    
    title = chat.title
    msg = f"#{action}\n<b>Chat:</b> {title}"

    if user:
        user_mention = user.mention_html()
        user_id = user.id

        msg = f"{msg}\n<b>User:</b> {user_mention}\n<b>ID:</b> <code>{user_id}</code>"

    if victim:
        victim_mention = victim.mention_html()
        victim_id = victim.id

        msg = f"{msg}\n<b>Victim:</b> {victim_mention}\n<b>ID:</b> <code>{victim_id}</code>"

    if action:
        msg = f"{msg}\n<b>Action:</b> {action}"

    if reason:
        msg = f"{msg}\n<b>Reason:</b> {reason}"

    try:
        await Message.send_msg(log_channel, msg)
    except Exception as e:
        logger.error(f"Error: {e}")


async def track_my_chat_activities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    this will check bot status (where it get banned or added or started or blocked etc.)
    """
    chat = update.effective_chat
    my_chat_member = update.my_chat_member
    user = my_chat_member.from_user # cause user

    _chk_stat = await _chat_member_status(my_chat_member) # True means user exist and False is not exist

    if not _chk_stat:
        return
    
    bot_exist, reason = _chk_stat

    if chat.type == "private":
        find_user = await MongoDB.find_one("users", "user_id", user.id)
        if not find_user:
            data = {
                "user_id": user.id,
                "Name": user.full_name,
                "username": user.username,
                "mention": user.mention_html(),
                "lang": user.language_code
            }
            try:
                await MongoDB.insert_single_data("users", data)
            except Exception as e:
                logger.error(f"Error: {e}")

    elif chat.type in ["group", "supergroup"]:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
        if not find_group:
            try:
                data = {
                    "chat_id": chat.id,
                    "title": chat.title
                }
                await MongoDB.insert_single_data("groups", data)
            except Exception as e:
                logger.error(f"Error: {e}")
                await Message.send_msg(chat.id, f"⚠ Group has not registered! Error: {e}")
                return
        if bot_exist:
            try:
                msg = (
                    "Thanks for adding me in this nice chat!\n\n"
                    "Please make me admin in chat, so I can help you managing this chat effectively!\n/help for bot help..."
                )
                await Message.send_msg(chat.id, msg)
                await Message.send_msg(user.id, f"You have added me in {chat.title}\nChatID: <code>{chat.id}</code>")
            except Exception as e:
                logger.error(f"Error: {e}")
    else:
        if bot_exist:
            try:
                await Message.send_msg(user.id, f"You have added me in {chat.title}\nChatID: <code>{chat.id}</code>")
            except Exception as e:
                logger.error(f"Error: {e}")


async def track_chat_activities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    this will check chat status (if any user joined or left etc.)
    """
    chat = update.effective_chat
    chat_member = update.chat_member

    user = chat_member.from_user # cause user
    victim = chat_member.new_chat_member.user

    try:
        find_group = context.chat_data["db_chat_data"]
    except Exception as e:
        logger.error(f"Error: {e}")

        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
        if find_group:
            context.chat_data["db_chat_data"] = find_group
        else:
            return

    welcome_msg = find_group.get("welcome_msg")
    custom_welcome_msg = find_group.get("custom_welcome_msg")
    goodbye_msg = find_group.get("goodbye_msg")
    antibot = find_group.get("antibot")

    _chk_stat = await _chat_member_status(chat_member) #True means user exist and False is not exist

    if not _chk_stat:
        return
    
    user_exist, reason = _chk_stat

    if user_exist == True:
        if victim.is_bot and antibot:
            _chk_per = await _check_permission(update, victim, user)

            if not _chk_per:
                return
            
            _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

            if bot_permission.status != ChatMember.ADMINISTRATOR:
                await Message.send_msg(chat.id, "<b>Antibot:</b> I'm not an admin in this chat!")
                return
            
            if victim_permission.status == ChatMember.ADMINISTRATOR:
                await Message.send_msg(chat.id, f"<b>Antibot:</b> {victim.mention_html()} has been added as an admin. I can't ban an admin!")
                return
            
            try:
                await bot.ban_chat_member(chat.id, victim.id)
                await Message.send_msg(chat.id, f"Antibot has banned {victim.mention_html()} from this chat!")
                await _log_channel(context, chat, user, victim, action="ANITBOT")
            except Exception as e:
                logger.error(f"Error: {e}")
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
            await _log_channel(context, chat, user, victim, action="JOIN")
    elif user_exist == False and reason == "left" and goodbye_msg:
        await Message.send_msg(chat.id, f"{victim.mention_html()} just left the chat...")
        await _log_channel(context, chat, user, victim, action="LEFT")


async def func_invite_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command will get invite link of the chat!\nAdd me to manage the chat!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return

    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_invite_users"):
            await Message.reply_msg(update, "You don't have enough rights to invite users in this chat!")
            return
    
    try:
        invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)

        if chat.link:
            msg = (
                f"Chat public link: {chat.link}\n"
                f"Chat invite link: {invite_link.invite_link}\n"
                f"Generated by: {user.mention_html()}"
            )
        else:
            msg = (
                f"Chat invite link: {invite_link.invite_link}\n"
                f"Generated by: {user.mention_html()}"
            )

        await Message.reply_msg(update, msg)
        await _log_channel(context, chat, user, action="INVITE")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    admin_title = " ".join(context.args)

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_promote_members"):
            await Message.reply_msg(update, "You don't have enough rights to promote/demote chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to promote!\nTo set admin_title eg. <code>/promote admin_title</code>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "The user is already an admin!")
        return
    
    try:
        await bot.promote_chat_member(chat.id, victim.id, can_manage_video_chats=True)
        msg = f"{user.mention_html()} has promoted user {victim.mention_html()} in this chat!"
        if admin_title:
            await bot.set_chat_administrator_custom_title(chat.id, victim.id, admin_title)
            msg = f"{msg}\nAdmin title: {admin_title}"
        await Message.reply_msg(update, msg)
        await _log_channel(context, chat, user, victim, action="PROMOTE")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_promote_members"):
            await Message.reply_msg(update, "You don't have enough rights to promote/demote chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to demote!")
        return
    
    try:
        await bot.promote_chat_member(chat.id, victim.id)
        await Message.reply_msg(update, f"{user.mention_html()} has demoted user {victim.mention_html()} in this chat!")
        await _log_channel(context, chat, user, victim, action="DEMOTE")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_pin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    msg_id = reply.message_id if reply else None

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command will pin replied message loudly in the chat!\nAdd me to manage the chat!", btn)
        return

    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_pin_messages"):
            await Message.reply_msg(update, "You don't have enough rights to pin/unpin messages!")
            return
    
    if not reply:
        await Message.reply_msg(update, "Please reply the message which one you want to pin loudly!")
        return
    
    try:
        await bot.pin_chat_message(chat.id, msg_id)
        await Message.reply_msg(update, f"Message pinned & notified everyone!")
        await _log_channel(context, chat, user, action="PIN")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_unpin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    reply = update.message.reply_to_message
    msg_id = reply.message_id if reply else None
    msg = " ".join(context.args)

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per


    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command will unpin replied message in the chat!\nUse <code>/unpin all</code> to unpin all pinned messages of chat!\nAdd me to manage the chat!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_pin_messages"):
            await Message.reply_msg(update, "You don't have enough rights to pin/unpin messages!")
            return
    
    if msg == "all":
        if user_permission.status != ChatMember.OWNER:
            await Message.reply_msg(update, "❌ This command is only for chat owner!")
            return
        
        context.chat_data["chat_id"] = chat.id
        context.chat_data["user_id"] = user.id
        context.chat_data["del_msg_pointer"] = e_msg
        
        btn_name = ["⚠ YES", "🍀 NO"]
        btn_data = ["unpin_all", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)
        try:
            await Message.reply_msg(update, f"Do you really want to unpin all messages of this chat?", btn)
            await _log_channel(context, chat, user, action="UNPIN_ALL")
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.send_msg(chat.id, f"Error: {e}")
        return

    if not reply:
        await Message.reply_msg(update, "This command will unpin replied message!\nUse <code>/unpin all</code> to unpin all pinned messages of chat!")
        return
    
    try:
        await bot.unpin_chat_message(chat.id, msg_id)
        await Message.reply_msg(update, f"Message unpinned!")
        await _log_channel(context, chat, user, action="UNPIN")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to ban!\nTo mention with reason eg. <code>/ban reason</code>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "I'm not going to ban an admin! You must be joking!")
        return
    
    if victim_permission.status == ChatMember.BANNED:
        await Message.reply_msg(update, "The user is already banned in this chat!")
        return
    
    try:
        await bot.ban_chat_member(chat.id, victim.id)
        msg = f"{user.mention_html()} has banned user {victim.mention_html()} from this chat!"
        if reason:
            msg = f"{msg}\nReason: {reason}"
        await Message.reply_msg(update, msg)
        await _log_channel(context, chat, user, victim, action="BAN", reason=reason)
        try:
            msg = f"{user.mention_html()} has banned you from {chat.title}!"
            if reason:
                msg = f"{msg}\nReason: {reason}"
            await Message.send_msg(victim.id, msg)
        except Exception as e:
            logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return
    
    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per


    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to unban!\nTo mention with reason eg. <code>/unban reason</code>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"Chat admin's can't be banned or unbanned.")
        return
    
    if victim_permission.status != ChatMember.BANNED:
        await Message.reply_msg(update, "The user isn't banned, so how could I unban?")
        return
    
    try:
        await bot.unban_chat_member(chat.id, victim.id)
        msg = f"{user.mention_html()} has unbanned user {victim.mention_html()}!"
        if reason:
            msg = f"{msg}\nReason: {reason}"
        await Message.reply_msg(update, msg)
        await _log_channel(context, chat, user, victim, action="UNBAN", reason=reason)
        try:
            invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)
            msg = f"{user.mention_html()} has unbanned you in {chat.title}!\nInvite Link: {invite_link.invite_link}"
            if reason:
                msg = f"{msg}\nReason: {reason}"
            await Message.send_msg(victim.id, msg)
        except Exception as e:
            logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per


    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to kick!\nTo mention with reason eg. <code>/kick reason</code>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"I'm not going to kick an admin! You must be joking!")
        return
    
    if victim_permission.status != ChatMember.MEMBER:
        await Message.reply_msg(update, "The user isn't a member in this chat!")
        return
    
    try:
        await bot.ban_chat_member(chat.id, victim.id)
        await bot.unban_chat_member(chat.id, victim.id)
        msg = f"{user.mention_html()} has kicked user {victim.mention_html()} from this chat!"
        if reason:
            msg = f"{msg}\nReason: {reason}"
        await Message.reply_msg(update, msg)
        try:
            invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)
            msg = f"{user.mention_html()} has kicked you from {chat.title}!\nInvite Link: {invite_link.invite_link}"
            if reason:
                msg = f"{msg}\nReason: {reason}"
            await Message.send_msg(victim.id, msg)
            await _log_channel(context, chat, user, victim, action="KICK", reason=reason)
        except Exception as e:
            logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_kickme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    victim = user

    await _check_del_cmd(update, context)

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]: 
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"I'm not going to kick you! You must be joking!")
        return
    
    try:
        await bot.ban_chat_member(chat.id, victim.id)
        await Message.reply_msg(update, f"Nice Choice! Get out of my sight!\n{victim.mention_html()} has choosed the easy way to out!")
        await bot.unban_chat_member(chat.id, victim.id)
        await _log_channel(context, chat, user, victim, action="KICKME")
        try:
            invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)
            await Message.send_msg(victim.id, f"You kicked yourself from {chat.title}!\nInvite Link: {invite_link.invite_link}")
        except Exception as e:
            logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
        
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to mute!\nTo mention with reason eg. <code>/mute reason</code>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"I'm not going to mute an admin! You must be joking!")
        return
    
    if victim_permission.status == ChatMember.RESTRICTED:
        await Message.reply_msg(update, "The user is already muted in this chat!")
        return
    
    permissions = {
        "can_send_other_messages": False,
        "can_invite_users": False,
        "can_send_polls": False,
        "can_send_messages": False,
        "can_change_info": False,
        "can_pin_messages": False,
        "can_add_web_page_previews": False,
        "can_manage_topics": False,
        "can_send_audios": False,
        "can_send_documents": False,
        "can_send_photos": False,
        "can_send_videos": False,
        "can_send_video_notes": False,
        "can_send_voice_notes": False
    }

    try:
        await bot.restrict_chat_member(chat.id, victim.id, permissions)
        msg = f"{user.mention_html()} has muted user {victim.mention_html()}!"
        if reason:
            msg = f"{msg}\nReason: {reason}"
        await Message.reply_msg(update, msg)
        await _log_channel(context, chat, user, victim, action="MUTE", reason=reason)
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict chat member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the member whom you want to unmute!\nTo mention with reason eg. <code>/unmute reason</code>")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"Chat admin's can't be muted or unmuted!")
        return
    
    if victim_permission.status != ChatMember.RESTRICTED:
        await Message.reply_msg(update, "The user isn't muted, so how could I unmute?")
        return
    
    permissions = {
        "can_send_other_messages": True,
        "can_invite_users": True,
        "can_send_polls": True,
        "can_send_messages": True,
        "can_change_info": True,
        "can_pin_messages": True,
        "can_add_web_page_previews": True,
        "can_manage_topics": True,
        "can_send_audios": True,
        "can_send_documents": True,
        "can_send_photos": True,
        "can_send_videos": True,
        "can_send_video_notes": True,
        "can_send_voice_notes": True
    }

    try:
        await bot.restrict_chat_member(chat.id, victim.id, permissions)
        msg = f"{user.mention_html()} has unmuted user {victim.mention_html()}!"
        if reason:
            msg = f"{msg}\nReason: {reason}"
        await Message.reply_msg(update, msg)
        await _log_channel(context, chat, user, victim, action="UNMUTE", reason=reason)
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_del(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    reason = " ".join(context.args)

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_delete_messages"):
            await Message.reply_msg(update, "You don't have enough rights to delete chat messages!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know which message to delete! Reply the message that you want to delete!\nTo mention with reason eg. <code>/del reason</code>")
        return

    try:
        message_to_del = [e_msg, reply]
        for delete_msg in message_to_del:
            await Message.del_msg(chat.id, delete_msg)
        msg = f"{victim.mention_html()}, your message is deleted by {user.mention_html()}!"
        if reason:
            msg = f"{msg}\nReason: {reason}"
        await Message.send_msg(chat.id, msg)
        await _log_channel(context, chat, user, victim, action="MSG_DEL", reason=reason)
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_lockchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command will remove all permissions of chat! No one will be able to send message etc.\nAdd me to manage the chat!", btn)
        return
        
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_change_info"):
            await Message.reply_msg(update, "You don't have enough rights to manage this chat!")
            return
    
    permissions = {
        "can_send_messages": False,
        "can_send_other_messages": False,
        "can_add_web_page_previews": False,
        "can_send_audios": False,
        "can_send_documents": False,
        "can_send_photos": False,
        "can_send_videos": False,
        "can_send_video_notes": False,
        "can_send_voice_notes": False,
        "can_send_polls": False
    }

    try:
        await bot.set_chat_permissions(chat.id, permissions)
        await Message.send_msg(chat.id, f"This chat has been Locked!\nEffective admin: {user.mention_html()}")
        await _log_channel(context, chat, user, action="CHAT_LOCK")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_unlockchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command will restore all permissions of chat! Everyone will be able to send message etc.\nAdd me to manage the chat!", btn)
        return
        
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_change_info"):
            await Message.reply_msg(update, "You don't have enough rights to manage this chat!")
            return
                    
    permissions = {
        "can_send_messages": True,
        "can_send_other_messages": True,
        "can_add_web_page_previews": True,
        "can_send_audios": True,
        "can_send_documents": True,
        "can_send_photos": True,
        "can_send_videos": True,
        "can_send_video_notes": True,
        "can_send_voice_notes": True,
        "can_send_polls": True
    }

    try:
        await bot.set_chat_permissions(chat.id, permissions)
        await Message.send_msg(chat.id, f"This chat has been Unlocked!\nEffective admin: {user.mention_html()}")
        await _log_channel(context, chat, user, action="CHAT_UNLOCK")
    except Exception as e:
        logger.error(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    reply = update.message.reply_to_message
    value = reply.text_html or reply.caption if reply else None
    keyword = " ".join(context.args)

    await _check_del_cmd(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "To set custom message/commands in group chat!\nAdd me to manage the chat!", btn)
        return
        
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_change_info"):
            await Message.reply_msg(update, "You don't have enough rights to manage this chat!")
            return
    
    if not value and not keyword:
        msg = (
            "To set custom message/command follow the instruction below...\n\n"
            "Reply the message with command which one you want to set as value for your keyword/command!\n"
            "Example: <code>/filters hi or /hi</code> send this by replying any message! suppose the message is <code>Hi, How are you!</code>\n"
            "Next time if you say <blockquote>hi or /hi</blockquote> in chat, the bot will reply with <blockquote>Hi, How are you!</blockquote>\n"
            "To remove a filter, use <code>/filters existing_filter_keyword</code> (without reply) and exact keyword (with capital letter or small letter)\n"
            "To remove all filters, use <code>/filters rem_all</code>"
        )

        context.chat_data["user_id"] = user.id
        context.chat_data["chat_id"] = chat.id
        context.chat_data["del_msg_pointer"] = e_msg

        btn_name_row1 = ["See chat filters", "Text formats"]
        btn_data_row1 = ["filters", "text_formats"]

        btn_name_row2 = ["Close"]
        btn_data_row2 = ["close"]

        row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
        row2 = await Button.cbutton(btn_name_row2, btn_data_row2)

        btn = row1 + row2

        try:
            await Message.reply_msg(update, msg, btn)
        except Exception as e:
            logger.error(f"Error: {e}")
        return
    
    if not keyword:
        await Message.reply_msg(update, f"Please read the instruction carefully!\n/filters for instruction!")
        return

    try:
        find_group = context.chat_data["db_chat_data"]
    except Exception as e:
        logger.error(f"Error: {e}")

        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
        if find_group:
            context.chat_data["db_chat_data"] = find_group
        else:
            await Message.reply_msg(update, "⚠ Chat isn't registered! Ban/Block me from this chat then add me again, then try!")
            return
    
    filters = find_group.get("filters")

    if filters and keyword and not value:
        if keyword == "rem_all":
            await MongoDB.update_db("groups", "chat_id", chat.id, "filters", None)
            await Message.reply_msg(update, f"{user.mention_html()} has removed all filters of this chat!")
            db_chat_data = await MongoDB.find_one("groups", "chat_id", chat.id)
            context.chat_data["db_chat_data"] = db_chat_data
            return
        
        try:
            if keyword.lower() in filters:
                del filters[keyword]
                await MongoDB.update_db("groups", "chat_id", chat.id, "filters", filters)
                await Message.reply_msg(update, f"{user.mention_html()} has removed filter <code>{keyword}</code>!")
            else:
                await Message.reply_msg(update, "There is no such filter available for this chat to delete!\nIf you are looking for how to add filters?\n/filters for instruction!")
                return
            db_chat_data = await MongoDB.find_one("groups", "chat_id", chat.id)
            context.chat_data["db_chat_data"] = db_chat_data
        except Exception as e:
            logger.error(f"Error: {e}")
            await Message.reply_msg(update, f"Error: {e}")
        return
    
    if not value:
        await Message.reply_msg(update, f"Reply the message which one you want to set as value for {keyword}\n/filters for detail instruction!")
        return

    if not filters:
        data = {
            keyword: value
        }
        await MongoDB.update_db("groups", "chat_id", chat.id, "filters", data)
    else:
        filters[keyword] = value
        await MongoDB.update_db("groups", "chat_id", chat.id, "filters", filters)
    db_chat_data = await MongoDB.find_one("groups", "chat_id", chat.id)
    context.chat_data["db_chat_data"] = db_chat_data
    await Message.reply_msg(update, f"{user.mention_html()} has added filter <code>{keyword}</code>!")


async def func_adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    _bot_info = await bot.get_me()

    await _check_del_cmd(update, context)

    owner_storage = "<b>Owner:</b>\n"
    admins_storage = ""
    bots_storage = ""

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    admins = await bot.get_chat_administrators(chat.id)
    for admin in admins:
        custom_title = f"- {admin.custom_title}" if admin.custom_title else ""
        if admin.status == "creator":
            if admin.is_anonymous == True:
                owner_storage += f"» Ghost 👻 <i>{custom_title}</i>\n"
            else:
                owner_storage += f"» {admin.user.mention_html()} <i>{custom_title}</i>\n"
        elif admin.user.is_bot == True:
            bots_storage += f"» {admin.user.mention_html()} <i>{custom_title}</i>\n"
        else:
            if admin.is_anonymous == True:
                admins_storage += f"» Ghost 👻 <i>{custom_title}</i>\n"
            else:
                admins_storage += f"» {admin.user.mention_html()} <i>{custom_title}</i>\n"
    if admins_storage:
        admins_storage = f"\n<b>Admin's:</b>\n{admins_storage}"
    if bots_storage:
        bots_storage = f"\n<b>Bot's:</b>\n{bots_storage}"

    await Message.reply_msg(update, f"<b>{chat.title}</b>\n▬▬▬▬▬▬▬▬▬▬\n{owner_storage}{admins_storage}{bots_storage}")
