from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from bot import config
from bot.utils.database import MemoryDB

def require_sudo(func):
    """
    :returns list: list of sudo's including **owner_id**
    """
    @wraps(func)
    async def wraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        owner_id = config.owner_id
        sudo_users = MemoryDB.bot_data.get("sudo_users") or []

        if owner_id not in sudo_users:
            sudo_users.append(owner_id)
        
        if user.id not in sudo_users:
            await update.message.reply_text("Access denied!")
            return
        
        return await func(update, context)
    return wraper
