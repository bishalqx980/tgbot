from telegram import Update, InlineKeyboardButton, ChatMember
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helper import Message


async def func_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
        getper_victim = await chat.get_member(victim.id)
    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)
    getper_user = await chat.get_member(user.id)

    if chat.type in ["group", "supergroup"]:
        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_user.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                """
                if getper_user.status == ChatMember.OWNER:
                    title = "Owner"
                else:
                    title = "Admin"
                """
                if reply:
                    if getper_victim.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_victim.status != ChatMember.BANNED:
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
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
        getper_victim = await chat.get_member(victim.id)
    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)
    getper_user = await chat.get_member(user.id)

    if chat.type in ["group", "supergroup"]:
        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_user.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                """
                if getper_user.status == ChatMember.OWNER:
                    title = "Owner"
                else:
                    title = "Admin"
                """
                if reply:
                    if getper_victim.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_victim.status == ChatMember.BANNED:
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
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
        getper_victim = await chat.get_member(victim.id)
    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)
    getper_user = await chat.get_member(user.id)

    if chat.type in ["group", "supergroup"]:
        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_user.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                """
                if getper_user.status == ChatMember.OWNER:
                    title = "Owner"
                else:
                    title = "Admin"
                """
                if reply:
                    if getper_victim.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_victim.status == ChatMember.MEMBER:
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
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_kickme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    victim = user
    getper_victim = await chat.get_member(victim.id)
    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)

    if chat.type in ["group", "supergroup"]:
        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_victim.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
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
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
        getper_victim = await chat.get_member(victim.id)
    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)
    getper_user = await chat.get_member(user.id)

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
        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_user.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                """
                if getper_user.status == ChatMember.OWNER:
                    title = "Owner"
                else:
                    title = "Admin"
                """
                if reply:
                    if getper_victim.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_victim.status != ChatMember.RESTRICTED:
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
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to manage your Group!", btn)


async def func_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        victim = reply.from_user
        getper_victim = await chat.get_member(victim.id)
    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)
    getper_user = await chat.get_member(user.id)

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
        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_user.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                if getper_user.status == ChatMember.OWNER:
                    title = "Owner"
                else:
                    title = "Admin"
                if reply:
                    if getper_victim.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_victim.status == ChatMember.RESTRICTED:
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
                InlineKeyboardButton("Add me", f"http://t.me/{get_bot.username}?startgroup=start")
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
