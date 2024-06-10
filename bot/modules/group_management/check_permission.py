from telegram import Update, ChatMember
from bot import bot
from bot.helper.telegram_helper import Message


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
        await Message.del_msg(chat.id, del_msg)

    return _bot_info, bot_permission, user_permission, admin_rights, victim_permission
