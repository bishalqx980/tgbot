from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message, Button
from bot.helper.query_handlers.query_functions import QueryFunctions
from bot.helper.query_handlers.func_help_query import QueryBotHelp
from bot.helper.query_handlers.func_chat_settings_query import QueryChatSettings
from bot.helper.query_handlers.func_bot_settings_query import QueryBotSettings
from bot.helper.query_handlers.func_menu_query import QueryMenus
from bot.modules.database.combined_db import global_search
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.functions.power_users import _power_users


async def func_callbackbtn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat

    # query_none return
    if query.data == "query_none":
        return
    
    async def popup(msg):
        try:
            await query.answer(msg, True)
        except Exception as e:
            logger.error(e)
    
    async def del_query():
        try:
            await query.message.delete()
        except Exception as e:
            logger.error(e)
    
    # Get data_center
    data_center = await LOCAL_DATABASE.find_one("data_center", chat.id)

    # Check data in data_center
    if not data_center:
        await popup(f"{chat.id} wasn't found in data center!")
        await del_query()
        return
    
    # Check user_id in data_center
    user_id = data_center.get("user_id")
    if not user_id:
        await popup(f"{user_id} wasn't found in data center!")
        await del_query()
        return
    
    if query.data != "query_whisper": # query_whisper exception ...
        if user.id != user_id:
            await popup("Access Denied!")
            return
    
    # Get data from data center
    collection_name = data_center.get("collection_name")
    db_find = data_center.get("db_find")
    db_vlaue = data_center.get("db_vlaue")
    
    # Check on localdb if not found check on mongodb if not found show error
    db = await global_search(collection_name, db_find, db_vlaue)
    if db[0] == False:
        await Message.reply_msg(update, db[1])
        return
    
    find_chat = db[1]
    
    if query.data == "query_whisper":
        data = await LOCAL_DATABASE.find_one("data_center", chat.id)
        if not data:
            await popup("Data wasn't found...")
            await del_query()
            return
        
        whisper_data = data.get("whisper_data")

        user_whisper_data = whisper_data.get(f"@{user.username}") or whisper_data.get(user.id)
        if not user_whisper_data:
            await popup("This whisper isn't for you or whisper expired...!")
            return
        
        if user_whisper_data.get("whisper_user") not in {user.id, f"@{user.username}"}:
            await popup("This whisper isn't for you!")
            return
        
        await popup(user_whisper_data.get("whisper_msg"))
    # Youtube download ...
    elif query.data in ["mp4", "mp3"]:
        await LOCAL_DATABASE.insert_data("data_center", user.id, {"youtube_content_format": query.data})
    # Database editing query ...
    elif query.data in [
        "query_edit_value",
        "query_rm_value",
        "query_true",
        "query_false",
        "query_close"
    ]:
        if query.data == "query_edit_value":
            is_list, is_int = False, False
            data_center = await LOCAL_DATABASE.find_one("data_center", chat.id)
            edit_data_key = data_center.get("edit_data_key")
            
            if edit_data_key in ["images", "allowed_links"]:
                is_list = True
            elif edit_data_key in ["log_channel"]:
                is_int = True
            elif edit_data_key in ["sudo_users"]:
                is_list = True
                is_int = True
            
            await QueryFunctions.query_edit_value(chat.id, query, chat, is_list=is_list, is_int=is_int)
        elif query.data == "query_rm_value":
            await QueryFunctions.query_rm_value(chat.id, query)
        elif query.data == "query_true":
            await QueryFunctions.query_true(chat.id, query)
        elif query.data == "query_false":
            await QueryFunctions.query_false(chat.id, query)
        elif query.data == "query_close":
            await QueryFunctions.query_close(chat.id, query)
    # Help section ...
    elif query.data in [
        "query_help_group_management_p1",
        "query_help_group_management_p2",
        "query_help_ai",
        "query_help_misc_functions",
        "query_help_owner_functions",
        "query_help_bot_info"
    ]:
        if query.data == "query_help_group_management_p1":
            await QueryBotHelp._query_help_group_management_p1(update, query)
        elif query.data == "query_help_group_management_p2":
            await QueryBotHelp._query_help_group_management_p2(update, query)
        elif query.data == "query_help_ai":
            await QueryBotHelp._query_help_ai(update, query)
        elif query.data == "query_help_misc_functions":
            await QueryBotHelp._query_help_misc_functions(update, query)
        elif query.data == "query_help_owner_functions":
            await QueryBotHelp._query_help_owner_functions(update, query)
        elif query.data == "query_help_bot_info":
            await QueryBotHelp._query_help_bot_info(update, query)
    # Chat settings ...
    elif query.data in [
        "query_chat_lang",
        "query_chat_auto_tr",
        "query_chat_set_echo",
        "query_chat_welcome_user",
        "query_set_custom_welcome_msg",
        "query_chat_farewell_user",
        "query_chat_antibot",
        "query_chat_del_cmd",
        "query_chat_log_channel",
        "query_chat_links_behave",
        "query_chat_all_links",
        "query_chat_allowed_links",
        "query_d_links",
        "query_c_links",
        "query_none_links",
        "query_chat_ai_status"
    ]:
        if query.data == "query_chat_lang":
            await QueryChatSettings._query_chat_lang(update, query, chat, find_chat)
        if query.data == "query_chat_auto_tr":
            await QueryChatSettings._query_chat_auto_tr(update, query, chat, find_chat)
        elif query.data == "query_chat_set_echo":
            await QueryChatSettings._query_chat_set_echo(update, query, chat, find_chat)
        elif query.data == "query_chat_welcome_user":
            await QueryChatSettings._query_chat_welcome_user(update, query, chat, find_chat)
        elif query.data == "query_set_custom_welcome_msg":
            await QueryChatSettings._query_set_custom_welcome_msg(update, query, chat, find_chat)
        elif query.data == "query_chat_farewell_user":
            await QueryChatSettings._query_chat_farewell_user(update, query, chat, find_chat)
        elif query.data == "query_chat_antibot":
            await QueryChatSettings._query_chat_antibot(update, query, chat, find_chat)
        elif query.data == "query_chat_del_cmd":
            await QueryChatSettings._query_chat_del_cmd(update, query, chat, find_chat)
        elif query.data == "query_chat_log_channel":
            await QueryChatSettings._query_chat_log_channel(update, query, chat, find_chat)
        elif query.data == "query_chat_links_behave":
            await QueryChatSettings._query_chat_links_behave(update, query, chat, find_chat)
        elif query.data == "query_chat_all_links":
            await QueryChatSettings._query_chat_all_links(update, query, chat, find_chat)
        elif query.data == "query_chat_allowed_links":
            await QueryChatSettings._query_chat_allowed_links(update, query, chat, find_chat)
        elif query.data == "query_d_links":
            await QueryChatSettings._query_d_links(query, chat)
        elif query.data == "query_c_links":
            await QueryChatSettings._query_c_links(query, chat)
        elif query.data == "query_none_links":
            await QueryChatSettings._query_none_links(query, chat)
        elif query.data == "query_chat_ai_status":
            await QueryChatSettings._query_chat_ai_status(update, query, chat, find_chat)
    # Bot settings ...
    elif query.data in [
        "query_bot_pic",
        "query_welcome_img",
        "query_images",
        "query_support_chat",
        "query_server_url",
        "query_sudo",
        "query_shrinkme_api",
        "query_omdb_api",
        "query_weather_api",
        "query_pastebin_api",
        "query_restore_db",
        "query_confirm_restore_db"
    ]:
        if collection_name != "bot_docs":
            await popup("Session expired! Send command again...!")
            await del_query()
            return
        
        power_users = await _power_users()
        if user.id in power_users:
            if query.data == "query_bot_pic":
                await QueryBotSettings._query_bot_pic(update, query, user, find_chat)
            elif query.data == "query_welcome_img":
                await QueryBotSettings._query_welcome_img(update, query, user, find_chat)
            elif query.data == "query_images":
                await QueryBotSettings._query_images(update, query, user, find_chat)
            elif query.data == "query_support_chat":
                await QueryBotSettings._query_support_chat(update, query, user, find_chat)
            elif query.data == "query_server_url":
                await QueryBotSettings._query_server_url(update, query, user, find_chat)
            elif query.data == "query_sudo":
                await QueryBotSettings._query_sudo(update, query, user, find_chat)
            elif query.data == "query_shrinkme_api":
                await QueryBotSettings._query_shrinkme_api(update, query, user, find_chat)
            elif query.data == "query_omdb_api":
                await QueryBotSettings._query_omdb_api(update, query, user, find_chat)
            elif query.data == "query_weather_api":
                await QueryBotSettings._query_weather_api(update, query, user, find_chat)
            elif query.data == "query_pastebin_api":
                await QueryBotSettings._query_pastebin_api(update, query, user, find_chat)
            elif query.data == "query_restore_db":
                await QueryBotSettings._query_restore_db(update, query)
            elif query.data == "query_confirm_restore_db":
                await QueryBotSettings._query_confirm_restore_db(update, data_center)
    # Query menus ...
    elif query.data in [
        "query_help_menu",
        "query_chat_settings_menu",
        "query_bot_settings_menu"
    ]:
        if query.data == "query_help_menu":
            await QueryMenus._query_help_menu(update, query, user)
        elif query.data == "query_chat_settings_menu":
            await QueryMenus._query_chat_settings_menu(update, query, chat, find_chat)
        elif query.data == "query_bot_settings_menu":
            await QueryMenus._query_bot_settings_menu(update, query)
    # Query broadcast ...
    elif query.data in [
        "query_broadcast_forward_true",
        "query_broadcast_forward_false",
        "query_broadcast_pin_true",
        "query_broadcast_pin_false",
        "query_broadcast_done"
    ]:
        if query.data == "query_broadcast_forward_true":
            await LOCAL_DATABASE.insert_data("data_center", user_id, {"is_forward": True}, "broadcast")
        elif query.data == "query_broadcast_forward_false":
            await LOCAL_DATABASE.insert_data("data_center", user_id, {"is_forward": False}, "broadcast")
        elif query.data == "query_broadcast_pin_true":
            await LOCAL_DATABASE.insert_data("data_center", user_id, {"is_pin": True}, "broadcast")
        elif query.data == "query_broadcast_pin_false":
            await LOCAL_DATABASE.insert_data("data_center", user_id, {"is_pin": False}, "broadcast")
        elif query.data == "query_broadcast_done":
            await LOCAL_DATABASE.insert_data("data_center", user_id, {"is_done": True}, "broadcast")
        
        if query.data != "query_broadcast_done":
            localdb = await LOCAL_DATABASE.find_one("data_center", user.id)
            db_broadcast = localdb.get("broadcast")
            is_forward = db_broadcast.get("is_forward") or False
            is_pin = db_broadcast.get("is_pin") or False
            
            msg = (
                "<b><u>Broadcast</u></b>\n\n"
                f"Forward: <code>{is_forward}</code>\n"
                f"Pin message: <code>{is_pin}</code>"
            )

            btn_name_row1 = ["Forward?", "YES", "NO"]
            btn_data_row1 = ["query_none", "query_broadcast_forward_true", "query_broadcast_forward_false"]

            btn_name_row2 = ["Pin message?", "YES", "NO"]
            btn_data_row2 = ["query_none", "query_broadcast_pin_true", "query_broadcast_pin_false"]

            btn_name_row3 = ["Done", "Close"]
            btn_data_row3 = ["query_broadcast_done", "query_close"]

            row1 = await Button.cbutton(btn_name_row1, btn_data_row1, True)
            row2 = await Button.cbutton(btn_name_row2, btn_data_row2, True)
            row3 = await Button.cbutton(btn_name_row3, btn_data_row3, True)

            btn = row1 + row2 + row3

            await Message.edit_msg(update, msg, query.message, btn)
