from telegram import Update, InlineKeyboardButton, ChatMember
from telegram.ext import ContextTypes
from bot import bot
from bot.helper.telegram_helper import Message


async def func_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        hostage = reply.from_user
        getper_hostage = await chat.get_member(hostage.id)
    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)
    getper_user = await chat.get_member(user.id)

    if chat.type in ["group", "supergroup"]:
        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_user.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                if getper_user.status == ChatMember.OWNER:
                    title = "Owner"
                else:
                    title = "Admin"
                if reply:
                    if getper_hostage.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_hostage.status != ChatMember.BANNED:
                            ban = await bot.ban_chat_member(chat.id, hostage.id)
                            if ban:
                                await Message.reply_msg(update, f"Another one bites the dust!\n{title} {user.mention_html()} has banned user {hostage.mention_html()}!")
                            else:
                                await Message.reply_msg(update, "Something Went Wrong! 🤔")
                        else:
                            await Message.reply_msg(update, "User is already banned in this chat! 🙂")
                    else:
                        await Message.reply_msg(update, "I'm not going to ban an admin! You must be joking! 😝")
                else:
                    await Message.reply_msg(update, "🤧 I don't know who you are talking about! Reply the user whom you want to ban!")
            else:
                await Message.reply_msg(update, "😪 You aren't an admin of this chat!")
        else:
            await Message.reply_msg(update, "🙁 I'm not an admin in this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)


async def func_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        hostage = reply.from_user
        getper_hostage = await chat.get_member(hostage.id)
    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)
    getper_user = await chat.get_member(user.id)

    if chat.type in ["group", "supergroup"]:
        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_user.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                if getper_user.status == ChatMember.OWNER:
                    title = "Owner"
                else:
                    title = "Admin"
                if reply:
                    if getper_hostage.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_hostage.status == ChatMember.BANNED:
                            unban = await bot.unban_chat_member(chat.id, hostage.id)
                            if unban:
                                await Message.reply_msg(update, f"Well! Well!!\n{title} {user.mention_html()} has unbanned user {hostage.mention_html()}!\n{hostage.first_name} can join again!")
                            else:
                                await Message.reply_msg(update, "Something Went Wrong! 🤔")
                        else:
                            await Message.reply_msg(update, "User isn't banned in this chat! 🙂")
                    else:
                        await Message.reply_msg(update, f"{user.mention_html()} is gone mad! {user.first_name} is trying to unban an admin! 🤣")
                else:
                    await Message.reply_msg(update, "🤧 I don't know who you are talking about! Reply the user whom you want to unban!")
            else:
                await Message.reply_msg(update, "😪 You aren't an admin of this chat!")
        else:
            await Message.reply_msg(update, "🙁 I'm not an admin in this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)


async def func_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        hostage = reply.from_user
        getper_hostage = await chat.get_member(hostage.id)
    get_bot = await bot.get_me()
    getper_bot = await chat.get_member(get_bot.id)
    getper_user = await chat.get_member(user.id)

    if chat.type in ["group", "supergroup"]:
        if getper_bot.status == ChatMember.ADMINISTRATOR:
            if getper_user.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                if getper_user.status == ChatMember.OWNER:
                    title = "Owner"
                else:
                    title = "Admin"
                if reply:
                    if getper_hostage.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_hostage.status == ChatMember.MEMBER:
                            await bot.ban_chat_member(chat.id, hostage.id)
                            unban = await bot.unban_chat_member(chat.id, hostage.id)
                            if unban:
                                await Message.reply_msg(update, f"Damn!\n{title} {user.mention_html()} has kicked user {hostage.mention_html()}!")
                            else:
                                await Message.reply_msg(update, "Something Went Wrong! 🤔")
                        else:
                            await Message.reply_msg(update, "User isn't a member of this chat! 🙂")
                    else:
                        await Message.reply_msg(update, f"I'm not going to kick an admin! You must be joking! 😝")
                else:
                    await Message.reply_msg(update, "🤧 I don't know who you are talking about! Reply the user whom you want to kick!")
            else:
                await Message.reply_msg(update, "😪 You aren't an admin of this chat!")
        else:
            await Message.reply_msg(update, "🙁 I'm not an admin in this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)


async def func_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        hostage = reply.from_user
        getper_hostage = await chat.get_member(hostage.id)
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
                if getper_user.status == ChatMember.OWNER:
                    title = "Owner"
                else:
                    title = "Admin"
                if reply:
                    if getper_hostage.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_hostage.status != ChatMember.RESTRICTED:
                            mute = await bot.restrict_chat_member(chat.id, hostage.id, permissions)
                            if mute:
                                await Message.reply_msg(update, f"Shh...!\n{title} {user.mention_html()} has muted user {hostage.mention_html()}!")
                            else:
                                await Message.reply_msg(update, "Something Went Wrong! 🤔")
                        else:
                            await Message.reply_msg(update, "User is already muted in this chat! 🙂")
                    else:
                        await Message.reply_msg(update, f"I'm not going to mute an admin! You must be joking! 😝")
                else:
                    await Message.reply_msg(update, "🤧 I don't know who you are talking about! Reply the user whom you want to mute!")
            else:
                await Message.reply_msg(update, "😪 You aren't an admin of this chat!")
        else:
            await Message.reply_msg(update, "🙁 I'm not an admin in this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)


async def func_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply = update.message.reply_to_message
    if reply:
        hostage = reply.from_user
        getper_hostage = await chat.get_member(hostage.id)
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
                    if getper_hostage.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                        if getper_hostage.status == ChatMember.RESTRICTED:
                            mute = await bot.restrict_chat_member(chat.id, hostage.id, permissions)
                            if mute:
                                await Message.reply_msg(update, f"Good!\n{title} {user.mention_html()} has unmuted user {hostage.mention_html()}!\n{hostage.first_name} can speak again!")
                            else:
                                await Message.reply_msg(update, "Something Went Wrong! 🤔")
                        else:
                            await Message.reply_msg(update, "User isn't muted in this chat! 🙂")
                    else:
                        await Message.reply_msg(update, f"{user.mention_html()} is gone mad! {user.first_name} is trying to unmute an admin! 🤣")
                else:
                    await Message.reply_msg(update, "🤧 I don't know who you are talking about! Reply the user whom you want to unmute!")
            else:
                await Message.reply_msg(update, "😪 You aren't an admin of this chat!")
        else:
            await Message.reply_msg(update, "🙁 I'm not an admin in this chat!")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)


async def func_adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    get_bot = await bot.get_me()

    owner_storage = "<b>👑 Owner:</b>\n\n"
    admins_storage = ""
    bots_storage = ""

    if chat.type in ["group", "supergroup"]:
        admins = await bot.get_chat_administrators(chat.id)
        for admin in admins:
            if admin.status == "creator":
                if admin.is_anonymous == True:
                    owner_storage += f"» Anonymous\n"
                else:
                    owner_storage += f"» <a href='tg://user?id={admin.user.id}'>{admin.user.first_name}</a>\n"
            elif admin.user.is_bot == True:
                bots_storage += f"» <a href='tg://user?id={admin.user.id}'>{admin.user.first_name}</a>\n"
            else:
                if admin.is_anonymous == True:
                    admins_storage += f"» Anonymous\n"
                else:
                    admins_storage += f"» <a href='tg://user?id={admin.user.id}'>{admin.user.first_name}</a>\n"
        if admins_storage != "":
            admins_storage = f"\n<b>⚔ Admin's:</b>\n\n{admins_storage}"
        if bots_storage != "":
            bots_storage = f"\n<b>🤖 Bot's:</b>\n\n{bots_storage}"

        await Message.reply_msg(update, f"<b>{chat.title} admin's ✨</b>\n\n{owner_storage}{admins_storage}{bots_storage}")
    else:
        btn = [
            [
                InlineKeyboardButton("Add me to Group", f"http://t.me/{get_bot.username}?startgroup=start")
            ]
        ]
        await Message.send_msg(chat.id, "Add me to your Group to manage your Group!", btn)
