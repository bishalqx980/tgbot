from telegram.ext import ContextTypes
from telegram.helpers import create_deep_linked_url
from ....helper.button_maker import ButtonMaker

async def pm_error(context: ContextTypes.DEFAULT_TYPE, chat_id):
    """`chat_id` where you want to send this message"""
    btn = ButtonMaker.ubutton([{"Add me to your chat": create_deep_linked_url(context.bot.username, "help", True)}])
    await context.bot.send_message(chat_id, "This command is made to be used in group chats, not in pm!", reply_markup=btn)
