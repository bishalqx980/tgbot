from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
from bot.modules.utils import calc

async def func_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = re_msg.text or re_msg.caption if re_msg else " ".join(context.args)

    if not msg:
        await Message.reply_msg(update, "Use <code>/calc math</code>\nor reply the math with <code>/calc</code>\nE.g. <code>/calc (980 - 80) + 100 / 4 * 4 - 20</code>")
        return
    
    try:
        await Message.reply_msg(update, f"Calculation result: <code>{await calc(msg):.2f}</code>")
    except Exception as e:
        logger.error(e)
        await Message.reply_msg(update, f"Can't calc: {e}")
