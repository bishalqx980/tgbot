from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.helper.telegram_helper import Message
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
    
    # Youtube download ...
    if  query.data in ["mp4", "mp3"]:
        await LOCAL_DATABASE.insert_data("data_center", chat.id, {"edit_data_key": query.data})
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
        else:
            pass
    # Help section ...
    elif query.data in [
        "query_help_group_management",
        "query_help_ai",
        "query_help_misc_functions",
        "query_help_owner_functions"
    ]:
        if  query.data == "query_help_group_management":
            await QueryBotHelp._query_help_group_management(update, query)
        elif query.data == "query_help_ai":
            await QueryBotHelp._query_help_ai(update, query)
        elif query.data == "query_help_misc_functions":
            await QueryBotHelp._query_help_misc_functions(update, query)
        elif query.data == "query_help_owner_functions":
            await QueryBotHelp._query_help_owner_functions(update, query)
        else:
            pass
    # Chat settings ...
    elif query.data in [
        "query_chat_lang",
        "query_chat_auto_tr",
        "query_chat_set_echo",
        "query_chat_welcome_msg",
        "query_set_custom_welcome_msg",
        "query_chat_farewell_msg",
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
        elif query.data == "query_chat_welcome_msg":
            await QueryChatSettings._query_chat_welcome_msg(update, query, chat, find_chat)
        elif query.data == "query_set_custom_welcome_msg":
            await QueryChatSettings._query_set_custom_welcome_msg(update, query, chat, find_chat)
        elif query.data == "query_chat_farewell_msg":
            await QueryChatSettings._query_chat_farewell_msg(update, query, chat, find_chat)
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
        else:
            pass
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
        "query_restore_db",
        "confirm_restore_db"
    ]:
        power_users = await _power_users()
        if user.id in power_users:
            if query.data == "query_bot_pic":
                await QueryBotSettings._query_bot_pic(update, query, chat, find_chat)
            elif query.data == "query_welcome_img":
                await QueryBotSettings._query_welcome_img(update, query, chat, find_chat)
            elif query.data == "query_images":
                await QueryBotSettings._query_images(update, query, chat, find_chat)
            elif query.data == "query_support_chat":
                await QueryBotSettings._query_support_chat(update, query, chat, find_chat)
            elif query.data == "query_server_url":
                await QueryBotSettings._query_server_url(update, query, chat, find_chat)
            elif query.data == "query_sudo":
                await QueryBotSettings._query_sudo(update, query, chat, find_chat)
            elif query.data == "query_shrinkme_api":
                await QueryBotSettings._query_shrinkme_api(update, query, chat, find_chat)
            elif query.data == "query_omdb_api":
                await QueryBotSettings._query_omdb_api(update, query, chat, find_chat)
            elif query.data == "query_weather_api":
                await QueryBotSettings._query_weather_api(update, query, chat, find_chat)
            elif query.data == "query_restore_db":
                await QueryBotSettings._query_restore_db(update, query)
            elif query.data == "confirm_restore_db":
                await QueryBotSettings._query_confirm_restore_db(update, data_center)
            else:
                pass
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
        else:
            pass
