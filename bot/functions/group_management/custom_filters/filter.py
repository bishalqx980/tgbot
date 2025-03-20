from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.modules.database.common import database_search
from bot.modules.database import MemoryDB, MongoDB
from bot.helper.telegram_helpers.button_maker import ButtonMaker
from bot.functions.group_management.auxiliary.pm_error import pm_error
from bot.functions.group_management.auxiliary.fetch_chat_admins import fetch_chat_admins

async def func_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    effective_message = update.effective_message
    re_msg = effective_message.reply_to_message
    value = re_msg.text_html or re_msg.caption if re_msg else None
    keyword = " ".join(context.args).lower()
    
    if chat.type == ChatType.PRIVATE:
        await pm_error(chat.id)
        return
    
    if user.is_bot:
        await effective_message.reply_text("Who are you? I don't take commands from anonymous admins...!")
        return
    
    chat_admins = await fetch_chat_admins(chat, user_id=user.id)
    
    if not (chat_admins["is_user_admin"] or chat_admins["is_user_owner"]):
        await effective_message.reply_text("You aren't an admin in this chat!")
        return
    
    if chat_admins["is_user_admin"] and not chat_admins["is_user_admin"].can_change_info:
        await effective_message.reply_text("You don't have enough permission to manage this chat!")
        return
    
    if not value or not keyword:
        data = {
            "user_id": user.id,
            "chat_id": chat.id,
            "effective_message_id": effective_message.id
        }

        MemoryDB.insert_data("data_center", chat.id, data)

        text = (
            "To set filters for this chat follow the instruction below...\n"
            "<blockquote>Reply the message with /filter which one you want to set as value for your keyword!</blockquote>"
            "Example: <code>/filter hi</code> send this by replying any message! suppose the message is <code>Hi, How are you!</code>\n"
            "Next time if you say <code>Hi</code> in chat, the bot will reply with <code>Hi, How are you!</code>\n\n"
            "<i><b>Note:</b> Use comma for adding multiple filter. eg. <code>/filter hi, bye</code></i>\n\n"
            "<i>Ques: How to remove a filter?\n Ans: /remove for instruction...</i>\n\n"
            "<b><u>Text formatting</u></b>\n"
            "<code>{first}</code> first name\n"
            "<code>{last}</code> last name\n"
            "<code>{fullname}</code> fullname\n"
            "<code>{username}</code> username\n"
            "<code>{mention}</code> mention\n"
            "<code>{id}</code> id\n"
            "<code>{chatname}</code> chat title\n"
        )

        btn = ButtonMaker.cbutton([{"Close": "query_close"}])
        await effective_message.reply_text(text, reply_markup=btn)
        return

    response, database_data = database_search("groups", "chat_id", chat.id)
    if response == False:
        await effective_message.reply_text(database_data)
        return
    
    filters = database_data.get("filters")

    modified_keyword = keyword.split(",")
    keywords = []
    for i in modified_keyword:
        keywords.append(i.strip())

    if not filters:
        data = {}
        for keyword in keywords:
            data.update({keyword: value})
        MongoDB.update_db("groups", "chat_id", chat.id, "filters", data)
    
    else:
        for keyword in keywords:
            filters[keyword] = value
        MongoDB.update_db("groups", "chat_id", chat.id, "filters", filters)
    
    group_data = MongoDB.find_one("groups", "chat_id", chat.id)
    MemoryDB.insert_data("chat_data", chat.id, group_data)
    msg_keywords = ", ".join(keywords)
    
    await effective_message.reply_text(f"{msg_keywords} filters added!")
