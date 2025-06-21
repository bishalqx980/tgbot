import asyncio
from bot.helpers import BuildKeyboard
from bot.utils.database import MemoryDB

async def anonymousAdmin(chat, effective_message, timeout=10):
    """
    :param chat: `update.effective_chat`
    :param effective_message: `update.effective_message`
    :param timeout: waiting time in sec
    :returns User: `telegram.User`
    """
    anonymous_admin = None
    MemoryDB.insert(MemoryDB.DATA_CENTER, chat.id, {"anonymous_admin": None})

    btn = BuildKeyboard.cbutton([{"Verify": "admin_anonymous_verify"}])
    sent_message = await effective_message.reply_text(f"UwU, annoymous admin! Click on <code>Verify</code> to proceed next! Timeout: <code>{timeout}</code>", reply_markup=btn)

    for i in range(timeout):
        data_center = MemoryDB.data_center[chat.id]
        anonymous_admin = data_center.get("anonymous_admin")
        if anonymous_admin:
            break
        
        await asyncio.sleep(1)
    
    await sent_message.delete()
    if not anonymous_admin:
        try:
            await effective_message.delete()
        except:
            pass
        
    return anonymous_admin
