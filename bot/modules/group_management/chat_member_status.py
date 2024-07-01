from telegram import ChatMember, ChatMemberUpdated

async def _chat_member_status(chat_member_update: ChatMemberUpdated):
    dif = chat_member_update.difference()
    status = dif.get("status")
    if not status:
        return
    
    user_exist, cause = None, None
    old_status, new_status = status

    user_exist = False if new_status in [ChatMember.LEFT, ChatMember.BANNED] else True
    
    if old_status in [ChatMember.LEFT, ChatMember.BANNED] and new_status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR]:
        cause = "JOINED"
    elif old_status not in [ChatMember.RESTRICTED, ChatMember.LEFT, ChatMember.BANNED] and old_status and new_status == ChatMember.LEFT:
        cause ="LEFT"
    elif old_status != ChatMember.BANNED and new_status == ChatMember.BANNED:
        cause ="BANNED"
    elif old_status == ChatMember.BANNED and new_status != ChatMember.BANNED:
        cause = "UNBANNED"
    elif old_status != ChatMember.RESTRICTED and new_status == ChatMember.RESTRICTED:
        cause = "RESTRICTED"
    elif old_status == ChatMember.RESTRICTED and new_status != ChatMember.RESTRICTED:
        cause = "UNRESTRICTED"
    elif old_status != ChatMember.ADMINISTRATOR and new_status == ChatMember.ADMINISTRATOR:
        cause = "PROMOTED"
    elif old_status == ChatMember.ADMINISTRATOR and new_status != ChatMember.ADMINISTRATOR:
        cause = "DEMOTED"

    return user_exist, cause
