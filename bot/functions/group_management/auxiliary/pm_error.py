from bot.helper.telegram_helpers.button_maker import ButtonMaker

async def pm_error(context, chat_id):
    """`chat_id` where you want to send this message"""
    btn = ButtonMaker.ubutton([{"Add me to your chat": f"{context.bot.link}?startgroup=help"}])
    await context.bot.send_message(chat_id, "This command is made to be used in group chats, not in pm!", reply_markup=btn)
