from bot import bot
from bot.helper.telegram_helpers.telegram_helper import Message, Button

async def _pm_error(chat_id):
    btn = await Button.ubutton([{"Add me to your chat": f"{bot.link}?startgroup=help"}])
    await Message.send_message(chat_id, "This command is made to be used in group chats, not in pm!", btn=btn)
