from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.ping_url import ping_url


async def func_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = " ".join(context.args)

    if not url:
        await Message.reply_msg(update, "Use <code>/ping url</code>\nE.g. <code>/ping https://google.com</code>")
        return
    
    if url[0:4] != "http":
        url = f"http://{url}"

    sent_msg = await Message.reply_msg(update, f"Pinging {url}\nPlease wait...")
    ping = await ping_url(url)

    if ping[0] == None:
        await Message.edit_msg(update, ping[1], sent_msg)
        return

    res, ping_time, status_code = ping
    site_status = "offline"
    if status_code == 200:
        site_status = "online"

    msg = (
        f"Site: {url}\n"
        f"R.time(ms): <code>{ping_time}</code>\n"
        f"R.code: <code>{status_code}</code>\n"
        f"Status: {site_status}"
    )

    await Message.edit_msg(update, msg, sent_msg)
