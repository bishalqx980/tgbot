from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.utils import Utils

async def func_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    text = " ".join(context.args) or (re_msg.text or re_msg.caption if re_msg else None)

    if not text:
        await effective_message.reply_text("Use <code>/calc math</code>\nor reply the math with <code>/calc</code> command.\nE.g. <code>/calc (980 - 80) + 100 / 4 * 4 - 20</code>")
        return
    
    res, output = Utils.calculator(text)
    await effective_message.reply_text(f"Calculation: <code>{output}</code>" if res else f"Error: {output.msg}")
