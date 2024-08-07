from bot import bot
from bot.helper.telegram_helper import Message, Button

async def _pm_error(chat_id):
    _bot_info = await bot.get_me()
    btn_name = ["Add me to your Group"]
    btn_url = [f"http://t.me/{_bot_info.username}?startgroup=start"]
    btn = await Button.ubutton(btn_name, btn_url)
    await Message.send_msg(chat_id, "This command is made to be used in group chats, not in pm!", btn)
