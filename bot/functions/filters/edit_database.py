from bot.modules.database import MemoryDB

def edit_database(chat_id, user_id, text, message_id):
    """
    Gets `update_data_value` from Edit Value query action & retuns `True` if is_editing.\n
    :param chat_id: update.effective_chat.id
    :param user_id: update.effective_user.id
    :param normal_text: update.effective_message.text (without formatting)
    :param message_id: update.effective_message.id
    """
    data_center = MemoryDB.data_center.get(chat_id)
    if data_center and data_center.get("is_editing"):
        if user_id != data_center.get("user_id"): # Checking: is that same user?
            return
        
        try:
            data_value = int(text)
        except ValueError:
            data_value = text
        
        data = {
            "update_data_value": data_value,
            "message_id": message_id
        }

        MemoryDB.insert("data_center", chat_id, data)
        return True
