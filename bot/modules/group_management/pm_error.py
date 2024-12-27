from bot.helper.telegram_helper import Message, Button
from bot.modules.database.local_database import LOCAL_DATABASE

async def _pm_error(chat_id):
    _bot_info = await LOCAL_DATABASE.find("_bot_info")
    btn_data = {
        "Add me to your Group": f"{_bot_info.get('link')}?startgroup=start"
    }
    btn = await Button.ubutton(btn_data)
    await Message.send_msg(chat_id, "This command is made to be used in group chats, not in pm!", btn=btn)
