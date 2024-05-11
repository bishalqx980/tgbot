from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import ContextTypes
from bot import bot, logger
from bot.helper.telegram_helper import Message, Button
from bot.modules.mongodb import MongoDB


async def _check_permission(update: Update, victim=None, user=None):
    chat = update.effective_chat

    _bot = await bot.get_me()
    bot_permission = await chat.get_member(_bot.id)

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

    return _bot, bot_permission, user_permission, admin_rights, victim_permission


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


async def func_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    help_msg = (
        "This feature will welcome new user in your group!\n"
        "Use <code>/welcome on</code> to turn on.\n"
        "Use <code>/welcome off</code> to turn off.\n\n"
        #"You can set welcome message by replying your custom message (markdown supported)."
    )

    if chat.type not in ["group", "supergroup"]:
        _bot = await bot.get_me()
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, help_msg, btn)
        return
    
    find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

    if not find_group:
        await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
        return
    
    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin of this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_change_info"):
            await Message.reply_msg(update, "You don't have enough rights to change group info!")
            return
    
    if msg == "on":
        try:
            await MongoDB.update_db("groups", "chat_id", chat.id, "welcome_msg", "on")
            await Message.reply_msg(update, "Welcome message has been enabled in this chat!\nFrom now I will welcome new members in this group!")
        except Exception as e:
            logger.error(f"Error enabling welcome_msg: {e}")
            await Message.reply_msg(update, f"Error: {e}")
    elif msg == "off":
        try:
            await MongoDB.update_db("groups", "chat_id", chat.id, "welcome_msg", "off")
            await Message.reply_msg(update, "Welcome message has been disabled in this chat!\nI won't welcome new members in this group!")
        except Exception as e:
            logger.error(f"Error disabling welcome_msg: {e}")
            await Message.reply_msg(update, f"Error: {e}")
    else:
        await Message.reply_msg(update, help_msg)


async def func_goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    help_msg = (
        "This feature will notify you in group if any user lefts your group!\n\n"
        "Use <code>/goodbye on</code> to turn on.\n"
        "Use <code>/goodbye off</code> to turn off.\n\n"
        #"You can set goodbye message by replying your custom message (markdown supported)."
    )

    if chat.type not in ["group", "supergroup"]:
        _bot = await bot.get_me()
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, help_msg, btn)
        return
    
    find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

    if not find_group:
        await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
        return
    
    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin of this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_change_info"):
            await Message.reply_msg(update, "You don't have enough rights to change group info!")
            return
    
    if msg == "on":
        try:
            await MongoDB.update_db("groups", "chat_id", chat.id, "goodbye_msg", "on")
            await Message.reply_msg(update, "Goodbye message has been enabled in this chat!\nFrom now I will notify you in group if any user lefts your group!")
        except Exception as e:
            logger.error(f"Error enabling goodbye_msg: {e}")
            await Message.reply_msg(update, f"Error: {e}")
    elif msg == "off":
        try:
            await MongoDB.update_db("groups", "chat_id", chat.id, "goodbye_msg", "off")
            await Message.reply_msg(update, "Goodbye message has been disabled in this chat!\nI won't notify you if any user lefts your group!")
        except Exception as e:
            logger.error(f"Error disabling goodbye_msg: {e}")
            await Message.reply_msg(update, f"Error: {e}")
    else:
        await Message.reply_msg(update, help_msg)


async def func_antibot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)

    help_msg = (
        "This feature will prevent bots from joining in your group!\n"
        "Use <code>/antibot on</code> to turn on.\n"
        "Use <code>/antibot off</code> to turn off.\n"
    )

    if chat.type not in ["group", "supergroup"]:
        _bot = await bot.get_me()
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, help_msg, btn)
        return
    
    find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

    if not find_group:
        await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
        return
    
    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin of this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return

    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_change_info"):
            await Message.reply_msg(update, "You don't have enough rights to change group info!")
            return
    
    if msg == "on":
        try:
            await MongoDB.update_db("groups", "chat_id", chat.id, "antibot", "on")
            await Message.reply_msg(update, "Antibot has been enabled in this chat!\nFrom now I will protect your group from bots spam!")
        except Exception as e:
            logger.error(f"Error enabling antibot: {e}")
            await Message.reply_msg(update, f"Error: {e}")
    elif msg == "off":
        try:
            await MongoDB.update_db("groups", "chat_id", chat.id, "antibot", "off")
            await Message.reply_msg(update, "Antibot has been disabled in this chat!\nI won't protect your group from bots spam!")
        except Exception as e:
            logger.error(f"Error disabling antibot: {e}")
            await Message.reply_msg(update, f"Error: {e}")
    else:
        await Message.reply_msg(update, help_msg)


async def track_chat_activities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    chat_member = update.chat_member

    user = chat_member.from_user
    victim = chat_member.new_chat_member.user

    find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

    if not find_group:
        return

    welcome_msg = find_group.get("welcome_msg")
    goodbye_msg = find_group.get("goodbye_msg")
    antibot = find_group.get("antibot")

    _chk_stat = await _chat_member_status(chat_member) #True means user exist and False is not exist

    if not _chk_stat:
        return
    
    user_exist, reason = _chk_stat

    if user_exist == True:
        if victim.is_bot and antibot == "on":
            _chk_per = await _check_permission(update, victim, user)

            if not _chk_per:
                return
            
            _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

            if bot_permission.status != ChatMember.ADMINISTRATOR:
                await Message.send_msg(chat.id, "<b>Antibot:</b> I'm not an admin of this group!")
                return
            
            if victim_permission.status == ChatMember.ADMINISTRATOR:
                await Message.send_msg(chat.id, f"<b>Antibot:</b> {victim.mention_html()} has been added as an admin. I can't ban an admin!")
                return
            
            try:
                await bot.ban_chat_member(chat.id, victim.id)
                await Message.send_msg(chat.id, f"<b>Antibot</b> has banned {victim.mention_html()} from this group!")
            except Exception as e:
                logger.info(f"Error: {e}")
                await Message.send_msg(chat.id, f"Error: {e}")
        elif welcome_msg == "on":
            await Message.send_msg(chat.id, f"Hi, {victim.mention_html()}! Welcome to {chat.title}")
    elif user_exist == False and reason == "left" and goodbye_msg == "on":
        await Message.send_msg(chat.id, f"{victim.mention_html()} just left the group...")


async def func_invite_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This feature will get invite link of your group!\nAdd me to manage your group!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return

    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_invite_users"):
            await Message.reply_msg(update, "You don't have enough rights to invite users in group!")
            return
    
    try:
        invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)

        if chat.link:
            msg = (
                f"Group public link: {chat.link}\n"
                f"Group invite link: {invite_link.invite_link}\n"
                f"Generated by: {user.mention_html()}"
            )
        else:
            msg = (
                f"Group invite link: {invite_link.invite_link}\n"
                f"Generated by: {user.mention_html()}"
            )

        await Message.send_msg(chat.id, msg)
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_pin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    msg_id = reply.message_id if reply else None

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This feature will pin replied message loudly in your group!\nAdd me to manage your group!", btn)
        return

    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
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
        await Message.send_msg(chat.id, f"Message pinned & notified everyone!")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_unpin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    msg_id = reply.message_id if reply else None
    msg = " ".join(context.args)

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per


    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This feature will unpin replied message in your group!\nUse <code>/unpin all</code> to unpin all pinned messages of group!\nAdd me to manage your group!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_pin_messages"):
            await Message.reply_msg(update, "You don't have enough rights to pin/unpin messages!")
            return
    
    if msg == "all":
        if user_permission.status != ChatMember.OWNER:
            await Message.reply_msg(update, "❌ This command is only for group owner!")
            return
        
        context.chat_data["chat_id"] = chat.id
        btn_name = ["⚠ YES", "🍀 NO"]
        btn_data = ["unpin_all", "close"]
        btn = await Button.cbutton(btn_name, btn_data, True)
        await Message.reply_msg(update, f"Do you really want to unpin all messages of this group?", btn)
        return

    if not reply:
        await Message.reply_msg(update, "This feature will unpin replied message!\nUse <code>/unpin all</code> to unpin all pinned messages of group!")
        return
    
    try:
        await bot.unpin_chat_message(chat.id, msg_id)
        await Message.send_msg(chat.id, f"Message unpinned!")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def exe_func_unpin_all_msg(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id):
    await bot.unpin_all_chat_messages(chat_id)
    await Message.send_msg(chat_id, "All pinned messages has been unpinned successfully!")


async def func_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin of this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict group member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to ban!")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "I'm not going to ban an admin! You must be joking!")
        return
    
    if victim_permission.status == ChatMember.BANNED:
        await Message.reply_msg(update, "The user is already banned in this group!")
        return
    
    try:
        await bot.ban_chat_member(chat.id, victim.id)
        await Message.reply_msg(update, f"{user.mention_html()} has removed user {victim.mention_html()} from this group!")
        try:
            await Message.send_msg(victim.id, f"{user.mention_html()} has removed you from {chat.title}!")
        except Exception as e:
            logger.error(f"Error: {e}")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None
    
    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per


    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin of this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict group member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to unban!")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"Group admin's can't be banned or unbanned.")
        return
    
    if victim_permission.status != ChatMember.BANNED:
        await Message.reply_msg(update, "The user isn't banned, so how could I unban?")
        return
    
    try:
        await bot.unban_chat_member(chat.id, victim.id)
        await Message.reply_msg(update, f"{user.mention_html()} has unbanned user {victim.mention_html()}!")
        try:
            invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)
            await Message.send_msg(victim.id, f"{user.mention_html()} has unbanned you in {chat.title}!\nInvite Link: {invite_link.invite_link}")
        except Exception as e:
            logger.error(f"Error: {e}")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per


    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict group member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to kick!")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"I'm not going to kick an admin! You must be joking!")
        return
    
    if victim_permission.status != ChatMember.MEMBER:
        await Message.reply_msg(update, "The user isn't a member of this group!")
        return
    
    try:
        await bot.ban_chat_member(chat.id, victim.id)
        await bot.unban_chat_member(chat.id, victim.id)
        await Message.reply_msg(update, f"{user.mention_html()} has kicked user {victim.mention_html()} from this group!")
        try:
            invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)
            await Message.send_msg(victim.id, f"{user.mention_html()} has kicked you from {chat.title}!\nInvite Link: {invite_link.invite_link}")
        except Exception as e:
            logger.error(f"Error: {e}")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_kickme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    victim = user

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]: 
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this group!")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"I'm not going to kick you! You must be joking!")
        return
    
    try:
        await bot.ban_chat_member(chat.id, victim.id)
        await bot.unban_chat_member(chat.id, victim.id)
        await Message.reply_msg(update, f"Nice Choice! Get out of my sight!\n{victim.mention_html()} has choosed the easy way to out!")
        try:
            invite_link = await bot.create_chat_invite_link(chat.id, name=user.first_name)
            await Message.send_msg(victim.id, f"You kicked yourself from {chat.title}!\nInvite Link: {invite_link.invite_link}")
        except Exception as e:
            logger.error(f"Error: {e}")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this group!")
        return
        
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict group member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to mute!")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"I'm not going to mute an admin! You must be joking!")
        return
    
    if victim_permission.status == ChatMember.RESTRICTED:
        await Message.reply_msg(update, "The user is already muted in this group!")
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
        await Message.reply_msg(update, f"{user.mention_html()} has muted user {victim.mention_html()}!")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    victim = reply.from_user if reply else None

    _chk_per = await _check_permission(update, victim, user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This command is made to be used in group chats, not in pm!", btn)
        return
    
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_restrict_members"):
            await Message.reply_msg(update, "You don't have enough rights to restrict/unrestrict group member!")
            return
    
    if not reply:
        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to unmute!")
        return
    
    if victim_permission.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, f"Group admin's can't be muted or unmuted!")
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
        await Message.reply_msg(update, f"{user.mention_html()} has unmuted user {victim.mention_html()}!")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_lockchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This feature will remove all permissions of group! No one will be able to send message Etc.\nAdd me to manage your group!", btn)
        return
        
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_change_info"):
            await Message.reply_msg(update, "You don't have enough rights to manage group!")
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
        await Message.send_msg(chat.id, f"This group has been Locked!\nEffective admin: {user.mention_html()}")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_unlockchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot, bot_permission, user_permission, admin_rights, victim_permission = _chk_per

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
        btn = await Button.ubutton(btn_name, btn_url)
        await Message.send_msg(chat.id, "This feature will restore all permissions of group! Everyone will be able to send message Etc.\nAdd me to manage your group!", btn)
        return
        
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this group!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin of this group!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_change_info"):
            await Message.reply_msg(update, "You don't have enough rights to manage group!")
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
        await Message.send_msg(chat.id, f"This group has been Unlocked!\nEffective admin: {user.mention_html()}")
    except Exception as e:
        logger.info(f"Error: {e}")
        await Message.send_msg(chat.id, f"Error: {e}")


async def func_adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    _bot = await bot.get_me()

    owner_storage = "<b>Owner:</b>\n"
    admins_storage = ""
    bots_storage = ""

    if chat.type not in ["group", "supergroup"]:
        btn_name = ["Add me in Group"]
        btn_url = [f"http://t.me/{_bot.username}?startgroup=start"]
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
