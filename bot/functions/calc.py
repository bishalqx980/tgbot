from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.utils import calculator

async def func_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    re_msg = update.message.reply_to_message
    msg = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None)

    if not msg:
        await Message.reply_msg(update, "Use <code>/calc math</code>\nor reply the math with <code>/calc</code> command.\nE.g. <code>/calc (980 - 80) + 100 / 4 * 4 - 20</code>")
        return
    
    calc = await calculator(msg)
    res, output = calc
    msg = f"Calculation: <code>{output}</code>" if res else f"Error: {output}"
    await Message.reply_msg(update, msg)
