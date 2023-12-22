import requests
from telegram import Update
from telegram.constants import ParseMode

async def ping_url(update: Update, ping_url):
  text = await update.message.reply_text(f"Pinging...")
  try:
    response = requests.get(ping_url)
    if response.status_code == 200:
      ping_time = response.elapsed.total_seconds() * 1000
      ping_time = round(ping_time, 2)
      await text.edit_text(f"↻ <a href='{ping_url}'>Server</a> respond in {ping_time}ms", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
      await text.edit_text(f"⚠ <a href='{ping_url}'>Server</a> request timeout! Response: {response.status_code}", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
  except requests.RequestException as e:
    await text.edit_text(f"Error: {e}")