from telegram import ChatMember, ChatMemberUpdated

async def _chat_member_status(c_mem_update: ChatMemberUpdated):
    dif = c_mem_update.difference()
    status = dif.get("status")

    if not status:
        return
    
    user_exist = None
    cause = None

    old_status, new_status = status
    
    exist_logic = [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]

    user_exist = True if new_status in exist_logic else False
    
    if new_status == ChatMember.LEFT:
        cause = "LEFT"
    elif new_status == ChatMember.RESTRICTED:
        cause = "RESTRICTED"
    elif new_status == ChatMember.BANNED:
        cause = "BANNED"
    
    if old_status == ChatMember.BANNED and new_status in exist_logic or new_status == ChatMember.LEFT:
        cause = "UNBANNED"
    elif old_status in [ChatMember.LEFT, ChatMember.RESTRICTED, ChatMember.BANNED] and new_status in exist_logic:
        cause = "JOINED"

    return user_exist, cause
