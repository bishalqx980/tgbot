from bot.modules.database import MemoryDB

def edit_database(chat_id, user_id, message):
    """
    Gets `update_data_value` from Edit Value query action & retuns `True` if is_editing.\n
    :param chat_id: update.effective_chat.id
    :param user_id: update.effective_user.id
    :param message: update.effective_message (Message Property)
    """
    data_center = MemoryDB.data_center.get(chat_id)
    if data_center and data_center.get("is_editing"):
        if user_id != data_center.get("user_id"): # Checking: is that same user?
            return
        
        data_value = None
        
        try:
            data_value = int(message.text)
        except ValueError:
            data_value = message.text
        except:
            pass
        
        data = {
            "photo_file_id": message.photo[-1].file_id if message.photo else None, # used for broadcast (MemoryDB)
            "broadcast_text": message.text_html, # used forBroadcast (MemoryDB)
            "update_data_value": data_value, # used for MongoDB Editing
            "message_id": message.id # mostly to delete the message
        }

        MemoryDB.insert("data_center", chat_id, data)
        return True
