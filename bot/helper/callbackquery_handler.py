from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.helper.query_handlers.query_functions import QueryFunctions
from bot.helper.query_handlers.query_help import QueryBotHelp
from bot.helper.query_handlers.query_chat_settings import QueryChatSettings
from bot.helper.query_handlers.query_bot_settings import QueryBotSettings
from bot.helper.query_handlers.query_menu import QueryMenus
from bot.modules.database import MemoryDB
from bot.modules.database.common import database_search


async def validate_user(query, chat, user, prevent_unauth_access=True):
    """
    validates user and returns `datacenter`\n
    prevents unauthorized access if `prevent_unauth_access` if true\n
    returns `data_center` of `chat.id` else shows error
    """
    data_center = MemoryDB.data_center.get(chat.id)
    if not data_center:
        await query.answer(f"chat_id: {chat.id} wasn't found in data center!")
        await query.delete_message()
        return
    
    user_id = data_center.get("user_id")
    if not user_id:
        await query.answer(f"user_id: {user_id} wasn't found in data center!")
        await query.delete_message()
        return
    
    if prevent_unauth_access:
        if user.id != user_id:
            await query.answer("Access Denied!", True)
            return
    
    return data_center


async def get_chat_data(update, data_center):
    """
    input `data_center` returns `data`\n
    usually made to work after `validate_user` function
    """
    collection_name = data_center.get("collection_name")
    search_key = data_center.get("search_key")
    match_value = data_center.get("match_value")
    
    # Check on memory if not found check on mongodb if not found show error
    response, database_data = database_search(collection_name, search_key, match_value)
    if response == False:
        await update.effective_message.reply_text(database_data)
        return
    
    return database_data

# main function
async def callbackquery_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    effective_message = update.effective_message

    # query_none return
    if query.data == "query_none":
        await query.answer()
        return

    query_dict_chat_settings = {
        "query_chat_settings_menu": QueryMenus._query_chat_settings_menu,
        "query_chat_lang": QueryChatSettings._query_chat_lang,
        "query_chat_auto_tr": QueryChatSettings._query_chat_auto_tr,
        "query_chat_set_echo": QueryChatSettings._query_chat_set_echo,
        "query_chat_welcome_user": QueryChatSettings._query_chat_welcome_user,
        "query_set_custom_welcome_msg": QueryChatSettings._query_set_custom_welcome_msg,
        "query_chat_farewell_user": QueryChatSettings._query_chat_farewell_user,
        "query_chat_antibot": QueryChatSettings._query_chat_antibot,
        "query_chat_links_behave": QueryChatSettings._query_chat_links_behave,
        "query_chat_is_links_allowed": QueryChatSettings._query_chat_is_links_allowed,
        "query_chat_allowed_links_list": QueryChatSettings._query_chat_allowed_links_list
    }

    query_dict_chat_settings_2 = {
        "query_d_links": QueryChatSettings._query_d_links,
        "query_c_links": QueryChatSettings._query_c_links,
        "query_none_links": QueryChatSettings._query_none_links
    }

    query_dict_broadcast = {
        "query_broadcast_forward_true": {"is_forward": True},
        "query_broadcast_forward_false": {"is_forward": False},
        "query_broadcast_pin_true": {"is_pin": True},
        "query_broadcast_pin_false": {"is_pin": False},
        "query_broadcast_done": {"is_done": True}
    }

    query_dict_db_edit = {
        "query_edit_value": QueryFunctions.query_edit_value,
        "query_rm_value": QueryFunctions.query_rm_value,
        "query_true": QueryFunctions.query_true,
        "query_false": QueryFunctions.query_false,
        "query_close": QueryFunctions.query_close
    }


    
    elif (query.data in query_dict_chat_settings or
          query.data in query_dict_chat_settings_2):
        data_center = await validate_user(query, chat, user)
        if not data_center:
            return
        
        find_chat = await get_chat_data(update, data_center)
        if not find_chat:
            return
        
        if query.data in query_dict_chat_settings:
            handler = query_dict_chat_settings[query.data]
            await handler(update, find_chat)
        
        elif query.data in query_dict_chat_settings_2:
            handler = query_dict_chat_settings_2[query.data]
            await handler(update, context, query)
    
    elif (query.data in query_dict_bot_settings or
          query.data in query_dict_bot_settings_2 or
          query.data in query_dict_bot_settings_3):
        data_center = await validate_user(query, chat, user)
        if not data_center:
            return
        
        if data_center.get("collection_name") != "bot_data":
            await query.answer("Session expired!", True)
            await query.delete_message()
            return
        
        database_data = await get_chat_data(update, data_center)
        if not database_data:
            return
        
        if query.data in query_dict_bot_settings:
            handler = query_dict_bot_settings[query.data]
            await handler(update, database_data)
        
        elif query.data in query_dict_bot_settings_2:
            handler = query_dict_bot_settings_2[query.data]
            await handler(update)
        
        elif query.data in query_dict_bot_settings_3:
            handler = query_dict_bot_settings_3[query.data]
            await handler(update)
    
    elif query.data in query_dict_broadcast:
        data_center = await validate_user(query, chat, user)
        if not data_center:
            return
        
        user_id = data_center.get("user_id")
        data = query_dict_broadcast[query.data]

        data_center = MemoryDB.data_center.get(user_id)
        if data_center and data_center.get("broadcast"):
            data_center["broadcast"].update(data)
        
        else:
            MemoryDB.insert("data_center", user_id, {"broadcast": data})
        
        if query.data != "query_broadcast_done":
            data_center = MemoryDB.data_center.get(user.id)
            db_broadcast = data_center.get("broadcast")
            is_forward = db_broadcast.get("is_forward", False)
            is_pin = db_broadcast.get("is_pin", False)
            
            text = (
                "<b><u>Broadcast</u></b>\n\n"
                f"Forward: <code>{is_forward}</code>\n"
                f"Pin message: <code>{is_pin}</code>"
            )

            btn_data = [
                {"Forward?": "query_none", "YES": "query_broadcast_forward_true", "NO": "query_broadcast_forward_false"},
                {"Pin message?": "query_none", "YES": "query_broadcast_pin_true", "NO": "query_broadcast_pin_false"},
                {"Done": "query_broadcast_done", "Close": "query_close"}
            ]

            btn = ButtonMaker.cbutton(btn_data)

            if effective_message.text:
                await effective_message.edit_text(text, reply_markup=btn)
            elif effective_message.caption:
                await effective_message.edit_caption(text, reply_markup=btn)
    
    elif query.data in query_dict_db_edit:
        handler = query_dict_db_edit[query.data]

        if query.data == "query_edit_value":
            is_list, is_int = False, False
            data_center = await validate_user(query, chat, user)
            if not data_center:
                return
            
            update_data_key = data_center.get("update_data_key")

            if update_data_key in ["images", "allowed_links_list"]:
                is_list = True
            elif update_data_key in ["log_channel"]:
                is_int = True
            elif update_data_key in ["sudo_users"]:
                is_list = True
                is_int = True
            
            await handler(context, chat.id, query, is_list=is_list, is_int=is_int)
        elif query.data == "query_close":
            await handler(context, chat.id, query)
        else:
            await handler(chat.id, query)
    
    elif query.data == "query_whisper":
        data_center = await validate_user(query, chat, user, False)
        if not data_center:
            return
        
        whisper_data = data_center.get("whisper_data")

        user_whisper_data = whisper_data.get(f"@{user.username}") or whisper_data.get(user.id)
        if not user_whisper_data:
            await query.answer("This whisper isn't for you or whisper has expired!", True)
            return
        
        if user_whisper_data.get("whisper_user") not in {user.id, f"@{user.username}"}:
            await query.answer("This whisper isn't for you!", True)
            return
        
        await query.answer(user_whisper_data.get("whisper_msg"), True)
