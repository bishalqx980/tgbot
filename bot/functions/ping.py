import requests
from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message


async def func_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = " ".join(context.args)

    if not url:
        await Message.reply_message(update, "Use <code>/ping url</code>\nE.g. <code>/ping https://google.com</code>")
        return
    
    if url[0:4] != "http":
        url = f"http://{url}"

    sent_msg = await Message.reply_message(update, f"Pinging {url}\nPlease wait...")
    try:
        res = requests.get(url, timeout=3)
        if res:
            status_codes = {
                200: "✅ Online (OK)",
                201: "✅ Created",
                202: "✅ Accepted",
                204: "⚠️ No Content",
                301: "➡️ Moved Permanently",
                302: "➡️ Found (Redirect)",
                400: "❌ Bad Request",
                401: "🔒 Unauthorized",
                403: "🚫 Forbidden",
                404: "❌ Not Found",
                408: "⏳ Request Timeout",
                500: "🔥 Internal Server Error",
                502: "⚠️ Bad Gateway",
                503: "⚠️ Service Unavailable"
            }

            status = status_codes[res.status_code]
            msg = (
                f"Site: {url}\n"
                f"R.time: <code>{int(res.elapsed.total_seconds() * 1000)}ms</code>\n"
                f"R.code: <code>{res.status_code}</code>\n"
                f"Status: <code>{status}</code>"
            )
        else:
            msg = "Oops! Please try again or report the issue."
    except requests.Timeout as e:
        msg = "Error: Request timeout."
    except requests.ConnectionError as e:
        msg = "Error: Connection error."
    except Exception as e:
        msg = "Oops! Please try again or report the issue."

    await Message.edit_message(update, f"<b>{msg}</b>", sent_msg)
