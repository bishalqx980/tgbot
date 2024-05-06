from telegram import Update, InlineKeyboardButton, ChatMember, ChatMemberUpdated
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helper import Message
from bot.mongodb import MongoDB


async def _check_permission(update: Update, victim=None, user=None):
    chat = update.effective_chat

    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)

    getper_user = await chat.get_member(user.id) if user else None
    getper_victim = await chat.get_member(victim.id) if victim else None

    return get_bot, getper_bot, getper_user, getper_victim


async def _chat_member_status(c_mem_update: ChatMemberUpdated):
    dif = c_mem_update.difference()
    status = dif.get("status")

    if status:
        old_status = status[0]
        new_status = status[1]
        was_logic = [ChatMember.LEFT, ChatMember.RESTRICTED, ChatMember.BANNED]
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
        return user_exist, reason


async def func_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)
    get_bot = await bot.get_me()

    help_msg = (
        "This feature will welcome new user in your Group!\n\n"
        "Use <code>/welcome on</code> to turn on.\n"
        "Use <code>/welcome off</code> to turn off.\n\n"
        #"You can set welcome message by replying your custom message (markdown supported)."
    )

    if chat.type in ["group", "supergroup"]:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

        if find_group:
            chk_per = await _check_permission(update, user=user)
            if chk_per:
                if chk_per[1].status == ChatMember.ADMINISTRATOR:
                    if chk_per[2].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if msg == "on":
                            try:
                                await MongoDB.update_db("groups", "chat_id", chat.id, "welcome_msg", "on")
                                await Message.reply_msg(update, "Welcome message has been enabled in this chat!\nFrom now I will welcome new members in this Group!")
                            except Exception as e:
                                print(f"Error enabling welcome_msg: {e}")
                                await Message.reply_msg(update, f"Something Went Wrong!\nError: {e}")
                        elif msg == "off":
                            try:
                                await MongoDB.update_db("groups", "chat_id", chat.id, "welcome_msg", "off")
                                await Message.reply_msg(update, "Welcome message has been disabled in this chat!\nI won't welcome new members in this Group!")
                            except Exception as e:
                                print(f"Error disabling welcome_msg: {e}")
                                await Message.reply_msg(update, f"Something Went Wrong!\nError: {e}")
                        elif msg == "":
                            await Message.reply_msg(update, help_msg)
                    else:
                        await Message.reply_msg(update, "You aren't an admin of this Group!")
                else:
                    await Message.reply_msg(update, "I'm not an admin of this Group!")
        else:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, help_msg, btn)


async def func_goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)
    get_bot = await bot.get_me()

    help_msg = (
        "This feature will notify you in group if any user lefts your Group!\n\n"
        "Use <code>/goodbye on</code> to turn on.\n"
        "Use <code>/goodbye off</code> to turn off.\n\n"
        #"You can set goodbye message by replying your custom message (markdown supported)."
    )

    if chat.type in ["group", "supergroup"]:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

        if find_group:
            chk_per = await _check_permission(update, user=user)
            if chk_per:
                if chk_per[1].status == ChatMember.ADMINISTRATOR:
                    if chk_per[2].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if msg == "on":
                            try:
                                await MongoDB.update_db("groups", "chat_id", chat.id, "goodbye_msg", "on")
                                await Message.reply_msg(update, "Goodbye message has been enabled in this chat!\nFrom now I will notify you in group if any user lefts your Group!")
                            except Exception as e:
                                print(f"Error enabling goodbye_msg: {e}")
                                await Message.reply_msg(update, f"Something Went Wrong!\nError: {e}")
                        elif msg == "off":
                            try:
                                await MongoDB.update_db("groups", "chat_id", chat.id, "goodbye_msg", "off")
                                await Message.reply_msg(update, "Goodbye message has been disabled in this chat!\nI won't notify you if any user lefts your Group!")
                            except Exception as e:
                                print(f"Error disabling goodbye_msg: {e}")
                                await Message.reply_msg(update, f"Something Went Wrong!\nError: {e}")
                        elif msg == "":
                            await Message.reply_msg(update, help_msg)
                    else:
                        await Message.reply_msg(update, "You aren't an admin of this Group!")
                else:
                    await Message.reply_msg(update, "I'm not an admin of this Group!")
        else:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, help_msg, btn)


async def func_antibot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = " ".join(context.args)
    get_bot = await bot.get_me()

    help_msg = (
        "This feature will prevent bots from joining in your Group! [to get protection from spam]\n\n"
        "Use <code>/antibot on</code> to turn on.\n"
        "Use <code>/antibot off</code> to turn off.\n"
    )

    if chat.type in ["group", "supergroup"]:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)

        if find_group:
            chk_per = await _check_permission(update, user=user)
            if chk_per:
                if chk_per[1].status == ChatMember.ADMINISTRATOR:
                    if chk_per[2].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if msg == "on":
                            try:
                                await MongoDB.update_db("groups", "chat_id", chat.id, "antibot", "on")
                                await Message.reply_msg(update, "Antibot has been enabled in this chat!\nFrom now I will protect your group from bots spam!")
                            except Exception as e:
                                print(f"Error enabling antibot: {e}")
                                await Message.reply_msg(update, f"Something Went Wrong!\nError: {e}")
                        elif msg == "off":
                            try:
                                await MongoDB.update_db("groups", "chat_id", chat.id, "antibot", "off")
                                await Message.reply_msg(update, "Antibot has been disabled in this chat!\nI won't protect your group from bots spam!")
                            except Exception as e:
                                print(f"Error disabling antibot: {e}")
                                await Message.reply_msg(update, f"Something Went Wrong!\nError: {e}")
                        elif msg == "":
                            await Message.reply_msg(update, help_msg)
                    else:
                        await Message.reply_msg(update, "You aren't an admin of this Group!")
                else:
                    await Message.reply_msg(update, "I'm not an admin of this Group!")
        else:
            await Message.reply_msg(update, "⚠ Chat isn't registered! click /start to register...\nThen try again!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, help_msg, btn)


async def track_chat_activities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    chat_member = update.chat_member

    user = chat_member.from_user
    victim = chat_member.new_chat_member.user

    find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
    if find_group:
        # status
        welcome_msg = find_group.get("welcome_msg")
        goodbye_msg = find_group.get("goodbye_msg")
        antibot = find_group.get("antibot")

        check_status = await _chat_member_status(chat_member) #True means user exist and False is not exist
        if check_status[0] == True:
            if victim.is_bot and antibot == "on":
                chk_per = await _check_permission(update, victim)
                if chk_per:
                    if chk_per[1].status == ChatMember.ADMINISTRATOR:
                        if chk_per[3].status != ChatMember.ADMINISTRATOR:
                            ban = await bot.ban_chat_member(chat.id, victim.id)
                            if ban:
                                await Message.send_msg(chat.id, f"<b>Antibot</b> has banned {victim.mention_html()} from this Group!")
                        else:
                            await Message.send_msg(chat.id, f"<b>Antibot:</b> {victim.mention_html()} has been added as an admin. I can't ban an admin!")
                    else:
                        await Message.send_msg(chat.id, "<b>Antibot:</b> I'm not an admin of this Group!")
            elif welcome_msg == "on":
                await Message.send_msg(chat.id, f"Hi, {victim.mention_html()}! Welcome to {chat.title}")
        elif check_status[0] == False and check_status[1] == "left" and goodbye_msg == "on":
            await Message.send_msg(chat.id, f"{victim.mention_html()} just left the Group...")


async def func_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
    else:
        victim = None

    chk_per = await _check_permission(update, victim, user)

    if chk_per:
        if chat.type in ["group", "supergroup"]:
            if chk_per[1].status == ChatMember.ADMINISTRATOR:
                if chk_per[2].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                    """
                    if chk_per[2].status == ChatMember.OWNER:
                        title = "Owner"
                    else:
                        title = "Admin"
                    """
                    if reply:
                        if chk_per[3].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                            if chk_per[3].status != ChatMember.BANNED:
                                ban = await bot.ban_chat_member(chat.id, victim.id)
                                if ban:
                                    await Message.reply_msg(update, f"{user.mention_html()} has removed user {victim.mention_html()} from this Group!")
                                    try:
                                        await Message.send_msg(victim.id, f"{user.mention_html()} has removed you from {chat.title}!")
                                    except Exception as e:
                                        print(f"Error g_management: {e}")
                                else:
                                    await Message.reply_msg(update, "Something Went Wrong!")
                            else:
                                await Message.reply_msg(update, "The user is already banned in this Group!")
                        else:
                            await Message.reply_msg(update, "I'm not going to ban an admin! You must be joking!")
                    else:
                        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to ban!")
                else:
                    await Message.reply_msg(update, "You aren't an admin of this Group!")
            else:
                await Message.reply_msg(update, "I'm not an admin of this Group!")
        else:
            btn = [
                [
                    InlineKeyboardButton("Add me", f"http://t.me/{chk_per[0].username}?startgroup=start")
                ]
            ]
            await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
    else:
        victim = None
    
    chk_per = await _check_permission(update, victim, user)

    if chk_per:
        if chat.type in ["group", "supergroup"]:
            if chk_per[1].status == ChatMember.ADMINISTRATOR:
                if chk_per[2].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                    """
                    if chk_per[2].status == ChatMember.OWNER:
                        title = "Owner"
                    else:
                        title = "Admin"
                    """
                    if reply:
                        if chk_per[3].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                            if chk_per[3].status == ChatMember.BANNED:
                                unban = await bot.unban_chat_member(chat.id, victim.id)
                                if unban:
                                    await Message.reply_msg(update, f"{user.mention_html()} has unbanned user {victim.mention_html()}!")
                                    try:
                                        await Message.send_msg(victim.id, f"{user.mention_html()} has unbanned you in {chat.title}!")
                                    except Exception as e:
                                        print(f"Error g_management: {e}")
                                else:
                                    await Message.reply_msg(update, "Something Went Wrong!")
                            else:
                                await Message.reply_msg(update, "The user isn't banned, so how could I unban?")
                        else:
                            await Message.reply_msg(update, f"Group admin's can't be banned or unbanned.")
                    else:
                        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to unban!")
                else:
                    await Message.reply_msg(update, "You aren't an admin of this Group!")
            else:
                await Message.reply_msg(update, "I'm not an admin of this Group!")
        else:
            btn = [
                [
                    InlineKeyboardButton("Add me", f"http://t.me/{chk_per[0].username}?startgroup=start")
                ]
            ]
            await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
    else:
        victim = None

    chk_per = await _check_permission(update, victim, user)

    if chk_per:
        if chat.type in ["group", "supergroup"]:
            if chk_per[1].status == ChatMember.ADMINISTRATOR:
                if chk_per[2].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                    """
                    if chk_per[2].status == ChatMember.OWNER:
                        title = "Owner"
                    else:
                        title = "Admin"
                    """
                    if reply:
                        if chk_per[3].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                            if chk_per[3].status == ChatMember.MEMBER:
                                await bot.ban_chat_member(chat.id, victim.id)
                                unban = await bot.unban_chat_member(chat.id, victim.id)
                                if unban:
                                    await Message.reply_msg(update, f"{user.mention_html()} has kicked user {victim.mention_html()} from this Group!")
                                    try:
                                        await Message.send_msg(victim.id, f"{user.mention_html()} has kicked you from {chat.title}!")
                                    except Exception as e:
                                        print(f"Error g_management: {e}")
                                else:
                                    await Message.reply_msg(update, "Something Went Wrong!")
                            else:
                                await Message.reply_msg(update, "The user isn't a member of this Group!")
                        else:
                            await Message.reply_msg(update, f"I'm not going to kick an admin! You must be joking!")
                    else:
                        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to kick!")
                else:
                    await Message.reply_msg(update, "You aren't an admin of this Group!")
            else:
                await Message.reply_msg(update, "I'm not an admin in this Group!")
        else:
            btn = [
                [
                    InlineKeyboardButton("Add me", f"http://t.me/{chk_per[0].username}?startgroup=start")
                ]
            ]
            await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_kickme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    victim = user

    chk_per = await _check_permission(update, victim, user)

    if chk_per:
        if chat.type in ["group", "supergroup"]:
            if chk_per[1].status == ChatMember.ADMINISTRATOR:
                if chk_per[3].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                    await bot.ban_chat_member(chat.id, victim.id)
                    unban = await bot.unban_chat_member(chat.id, victim.id)
                    if unban:
                        await Message.reply_msg(update, f"Nice Choice! Get out of my sight!\n{victim.mention_html()} has choosed the easy way to out!")
                    else:
                        await Message.reply_msg(update, "Something Went Wrong!")
                else:
                    await Message.reply_msg(update, f"I'm not going to kick you! You must be joking!")
            else:
                await Message.reply_msg(update, "I'm not an admin in this Group!")
        else:
            btn = [
                [
                    InlineKeyboardButton("Add me", f"http://t.me/{chk_per[0].username}?startgroup=start")
                ]
            ]
            await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
    else:
        victim = None

    chk_per = await _check_permission(update, victim, user)

    if chk_per:
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

        if chat.type in ["group", "supergroup"]:
            if chk_per[1].status == ChatMember.ADMINISTRATOR:
                if chk_per[2].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                    """
                    if chk_per[2].status == ChatMember.OWNER:
                        title = "Owner"
                    else:
                        title = "Admin"
                    """
                    if reply:
                        if chk_per[3].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                            if chk_per[3].status != ChatMember.RESTRICTED:
                                mute = await bot.restrict_chat_member(chat.id, victim.id, permissions)
                                if mute:
                                    await Message.reply_msg(update, f"{user.mention_html()} has muted user {victim.mention_html()}!")
                                    try:
                                        await Message.send_msg(victim.id, f"{user.mention_html()} has muted you in {chat.title}!")
                                    except Exception as e:
                                        print(f"Error g_management: {e}")
                                else:
                                    await Message.reply_msg(update, "Something Went Wrong!")
                            else:
                                await Message.reply_msg(update, "The user is already muted in this Group!")
                        else:
                            await Message.reply_msg(update, f"I'm not going to mute an admin! You must be joking!")
                    else:
                        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to mute!")
                else:
                    await Message.reply_msg(update, "You aren't an admin of this Group!")
            else:
                await Message.reply_msg(update, "I'm not an admin in this Group!")
        else:
            btn = [
                [
                    InlineKeyboardButton("Add me", f"http://t.me/{chk_per[0].username}?startgroup=start")
                ]
            ]
            await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
    else:
        victim = None

    chk_per = await _check_permission(update, victim, user)

    if chk_per:
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

        if chat.type in ["group", "supergroup"]:
            if chk_per[1].status == ChatMember.ADMINISTRATOR:
                if chk_per[2].status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                    if chk_per[2].status == ChatMember.OWNER:
                        title = "Owner"
                    else:
                        title = "Admin"
                    if reply:
                        if chk_per[3].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                            if chk_per[3].status == ChatMember.RESTRICTED:
                                mute = await bot.restrict_chat_member(chat.id, victim.id, permissions)
                                if mute:
                                    await Message.reply_msg(update, f"{user.mention_html()} has unmuted user {victim.mention_html()}!")
                                else:
                                    await Message.reply_msg(update, "Something Went Wrong!")
                            else:
                                await Message.reply_msg(update, "The user isn't muted, so how could I unmute?")
                        else:
                            await Message.reply_msg(update, f"Group admin's can't be muted or unmuted!")
                    else:
                        await Message.reply_msg(update, "I don't know who you are talking about! Reply the user whom you want to unmute!")
                else:
                    await Message.reply_msg(update, "You aren't an admin of this Group!")
            else:
                await Message.reply_msg(update, "I'm not an admin in this Group!")
        else:
            btn = [
                [
                    InlineKeyboardButton("Add me", f"http://t.me/{chk_per[0].username}?startgroup=start")
                ]
            ]
            await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    get_bot = await bot.get_me()

    owner_storage = "<b>Owner:</b>\n"
    admins_storage = ""
    bots_storage = ""

    if chat.type in ["group", "supergroup"]:
        admins = await bot.get_chat_administrators(chat.id)
        for admin in admins:
            if admin.status == "creator":
                if admin.is_anonymous == True:
                    owner_storage += f"» Ghost 👻\n"
                else:
                    owner_storage += f"» {admin.user.mention_html()}\n"
            elif admin.user.is_bot == True:
                bots_storage += f"» {admin.user.mention_html()}\n"
            else:
                if admin.is_anonymous == True:
                    admins_storage += f"» Ghost 👻\n"
                else:
                    admins_storage += f"» {admin.user.mention_html()}\n"
        if admins_storage:
            admins_storage = f"\n<b>Admin's:</b>\n{admins_storage}"
        if bots_storage:
            bots_storage = f"\n<b>Bot's:</b>\n{bots_storage}"

        await Message.reply_msg(update, f"<b>{chat.title}</b>\n▬▬▬▬▬▬▬▬▬▬\n{owner_storage}{admins_storage}{bots_storage}")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to manage your Group!", btn)
