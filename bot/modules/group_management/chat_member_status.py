from telegram import ChatMember, ChatMemberUpdated

async def _chat_member_status(chat_member_update: ChatMemberUpdated):
    dif = chat_member_update.difference()
    status = dif.get("status")
    if not status:
        return
    
    user_exist, cause = None, None
    old_status, new_status = status
    
    exist_logic = [ChatMember.MEMBER, ChatMember.RESTRICTED, ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    not_exist_logic = [ChatMember.LEFT, ChatMember.BANNED]

    user_exist = True if old_status in not_exist_logic and new_status in exist_logic else False
    
    if new_status == ChatMember.LEFT:
        cause = "LEFT"
    elif new_status == ChatMember.RESTRICTED:
        cause = "RESTRICTED"
    elif new_status == ChatMember.BANNED:
        cause = "BANNED"
    elif old_status == ChatMember.BANNED and new_status in exist_logic or new_status == ChatMember.LEFT:
        cause = "UNBANNED"
    elif old_status in not_exist_logic and new_status in exist_logic:
        cause = "JOINED"

    return user_exist, cause
