from telegram import Message, User, Chat

async def autoTriggers(message: Message, user: User, chat: Chat, filters: dict):
    """
    :param message: `update.effective_message`
    :param user: `update.effective_user`
    :param chat: `update.effective_chat`
    :param filters: chat filters (from chat database)
    """
    text = message.text or message.caption

    for keyword in filters:
        try:
            filtered_text = text.lower()
        except AttributeError:
            filtered_text = text
        
        if keyword.lower() in filtered_text:
            filtered_text = filters.get(keyword)

            formattings = {
                "{first}": user.first_name,
                "{last}": user.last_name or "",
                "{fullname}": user.full_name,
                "{username}": user.name,
                "{mention}": user.mention_html(),
                "{id}": user.id,
                "{chatname}": chat.title
            }

            for key, value in formattings.items():
                filtered_text = filtered_text.replace(key, str(value))
            
            await message.reply_text(filtered_text)
