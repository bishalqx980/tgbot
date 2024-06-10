from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE


async def _log_channel(context: ContextTypes.DEFAULT_TYPE, chat, user, victim=None, action=None, reason=None):
    """
    sends chat actions to log channel
    """
    find_group = await LOCAL_DATABASE.find_one("groups", chat.id)
    if not find_group:
        find_group = await MongoDB.find_one("groups", "chat_id", chat.id)
        if find_group:
            await LOCAL_DATABASE.insert_data("groups", chat.id, find_group)
        else:
            return
    
    log_channel = find_group.get("log_channel")
    if not log_channel:
        return
    
    title = chat.title
    msg = f"#{action}\n<b>Chat:</b> {title}"

    if user:
        user_mention = user.mention_html()
        user_id = user.id

        msg = f"{msg}\n<b>User:</b> {user_mention}\n<b>ID:</b> <code>{user_id}</code>"

    if victim:
        victim_mention = victim.mention_html()
        victim_id = victim.id

        msg = f"{msg}\n<b>Victim:</b> {victim_mention}\n<b>ID:</b> <code>{victim_id}</code>"

    if action:
        msg = f"{msg}\n<b>Action:</b> {action}"

    if reason:
        msg = f"{msg}\n<b>Reason:</b> {reason}"

    try:
        await Message.send_msg(log_channel, msg)
    except Exception as e:
        logger.error(e)
