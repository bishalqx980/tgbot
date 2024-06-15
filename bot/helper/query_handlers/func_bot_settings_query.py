from telegram import Update
from telegram.ext import ContextTypes
from bot import logger
from bot.modules.database.local_database import LOCAL_DATABASE


async def func_bot_settings_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat

    async def popup(msg):
        await query.answer(msg, True)
    
    async def query_del():
        try:
            await query.delete_message()
        except Exception as e:
            logger.error(e)

    data_center = await LOCAL_DATABASE.find_one("data_center", chat.id)
    if not data_center:
        await popup(f"Error: {chat.id} wasn't found in data center! Try to send command again!")
        await query_del()
        return
    
    if chat.type != "private":
        user_id = data_center.get("user_id")
        if user.id != user_id:
            await popup("Access Denied!")
            return
    
    btn_name_row1 = ["Bot pic", "Welcome img"]
    btn_data_row1 = ["query_bot_pic", "query_welcome_img"]

    btn_name_row2 = ["Images", "Support chat"]
    btn_data_row2 = ["query_images", "query_support_chat"]

    btn_name_row3 = ["Server url", "Sudo"]
    btn_data_row3 = ["query_server_url", "query_sudo"]

    btn_name_row4 = ["Shrinkme API", "OMDB API", "Weather API"]
    btn_data_row4 = ["query_shrinkme_api", "query_omdb_api", "query_weather_api"]

    btn_name_row5 = ["⚠ Restore Settings", "Close"]
    btn_data_row5 = ["query_restore_db", "query_close"]
    
    if query.data == "query_bot_pic":
        pass
    elif query.data == "query_welcome_img":
        pass
    elif query.data == "query_images":
        pass
    elif query.data == "query_support_chat":
        pass
    elif query.data == "query_sudo":
        pass
    elif query.data == "query_bot_pic":
        pass
    elif query.data == "query_bot_pic":
        pass





