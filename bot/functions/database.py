import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.database.mongodb import MongoDB
from bot.helper.telegram_helper import Message
from bot.functions.power_users import _power_users


async def func_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    e_msg = update.effective_message

    power_users = await _power_users()
    if user.id not in power_users:
        await Message.reply_msg(update, "Access denied!")
        return
    
    if chat.type != "private":
        await Message.reply_msg(update, f"Boss you are in public chat!")
        await asyncio.sleep(3)
        await Message.del_msgs(chat.id, [e_msg.id, e_msg.id + 1])
        return
    
    db = await MongoDB.info_db()
    msg = "<b>Database\n――――――――</b>\n"
    for info in db:
        msg += (
            f"<b>Name</b>: <code>{info[0]}</code>\n"
            f"<b>Count</b>: <code>{info[1]}</code>\n"
            f"<b>Size</b>: <code>{info[2]}</code>\n"
            f"<b>A. size</b>: <code>{info[3]}</code>\n"
            f"<b>――――――――</b>\n"
        )
    
    active_status = await MongoDB.find("users", "active_status")
    active_users = active_status.count(True)
    inactive_users = active_status.count(False)
    await Message.reply_msg(update, f"{msg}<b>Active users</b>: <code>{active_users}</code>\n<b>Inactive users</b>: <code>{inactive_users}</code>")
