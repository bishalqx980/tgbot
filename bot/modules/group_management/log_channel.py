from telegram import Update
from bot.helper.telegram_helper import Message
from bot.modules.database.all_db_search import all_db_search

async def _log_channel(update: Update, chat, user, victim=None, action=None, reason=None):
    """
    sends chat actions to log channel
    """
    db = await all_db_search("groups", "chat_id", chat.id)
    if db[0] == False:
        await Message.reply_msg(update, db[1])
        return
    
    find_group = db[1]
    
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

    if reason:
        msg = f"{msg}\n<b>Reason:</b> {reason}"

    await Message.send_msg(log_channel, msg)
