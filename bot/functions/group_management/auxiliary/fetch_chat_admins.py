from telegram import ChatMember

async def fetch_chat_admins(chat, bot_id=None, user_id=None, victim_id=None):
    """
    :param chat: `update.effective_chat`
    :param bot_id: `context.bot.id`
    :param user_id: `update.effective_user.id`
    :param victim_id: `replied user id`\n
    returns: `dict`
    """
    chat_admins = await chat.get_administrators()

    is_user_admin = None
    is_user_owner = None

    is_victim_admin = None
    is_victim_owner = None

    is_bot_admin = None

    for admin in chat_admins:
        admin_id = admin.user.id
        admin_status = admin.status

        if user_id and admin_id == user_id:
            if admin_status == ChatMember.ADMINISTRATOR:
                is_user_admin = admin
            elif admin_status == ChatMember.OWNER:
                is_user_owner = admin
        
        if victim_id and admin_id == victim_id:
            if admin_status == ChatMember.ADMINISTRATOR:
                is_victim_admin = admin
            elif admin_status == ChatMember.OWNER:
                is_victim_owner = admin
        
        if bot_id and admin_id == bot_id:
            is_bot_admin = admin
    
    return {
        "is_user_admin": is_user_admin,
        "is_user_owner": is_user_owner,
        "is_victim_admin": is_victim_admin,
        "is_victim_owner": is_victim_owner,
        "is_bot_admin": is_bot_admin
    }
