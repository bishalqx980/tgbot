import aiohttp
from time import time
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
        start_time = time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_time = int((time() - start_time) * 1000)
                if response_time > 1000:
                    response_time = f"{(response_time / 1000):.2f}s"
                else:
                    response_time = f"{response_time}ms"
                
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

                status = status_codes.get(response.status, "⚠️ Unknown Status")
                msg = (
                    f"Site: {url}\n"
                    f"R.time: <code>{response_time}</code>\n"
                    f"R.code: <code>{response.status}</code>\n"
                    f"Status: <code>{status}</code>"
                )
    except aiohttp.ServerTimeoutError:
        msg = "Error: Request timeout."
    except aiohttp.ServerConnectionError:
        msg = "Error: Connection error."
    except Exception:
        msg = "Oops! Please try again or report the issue."

    await Message.edit_message(update, f"<b>{msg}</b>", sent_msg)
