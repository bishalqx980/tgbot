from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from bot.helper.telegram_helpers.telegram_helper import Message, Button
from bot.modules.database.common import database_search
from bot.modules.database import MemoryDB, MongoDB
from bot.functions.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.functions.group_management.check_permission import _check_permission


async def func_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    reply = update.message.reply_to_message
    value = reply.text_html or reply.caption if reply else None
    keyword = " ".join(context.args).lower()
    
    if chat.type == ChatType.PRIVATE:
        await _pm_error(chat.id)
        return
    
    await func_del_command(update, context)

    if user.is_bot:
        await Message.reply_message(update, "I don't take permission from anonymous admins!")
        return
    
    sent_msg = await Message.reply_message(update, "💭")
    _chk_per = await _check_permission(update, user=user)
    if not _chk_per:
        await Message.edit_message(update, "Oops! Please try again or report the issue.", sent_msg)
        return
        
    if _chk_per["bot_permission"].status != ChatMember.ADMINISTRATOR:
        await Message.edit_message(update, "I'm not an admin in this chat!", sent_msg)
        return
    
    if _chk_per["user_permission"].status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.edit_message(update, "You aren't an admin in this chat!", sent_msg)
        return
    
    if _chk_per["user_permission"].status == ChatMember.ADMINISTRATOR:
        if not _chk_per["user_permission"].can_change_info:
            await Message.edit_message(update, "You don't have enough rights to manage this chat!", sent_msg)
            return
    
    if not value or not keyword:
        data = {
            "user_id": user.id,
            "chat_id": chat.id,
            "collection_name": None,
            "db_find": None,
            "db_vlaue": None,
            "edit_data_key": None,
            "edit_data_value": None,
            "del_msg_pointer_id": e_msg.id,
            "edit_data_value_msg_pointer_id": None
        }

        MemoryDB.insert_data("data_center", chat.id, data)

        msg = (
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

        btn = await Button.cbutton([{"Close": "query_close"}])
        await Message.edit_message(update, msg, sent_msg, btn)
        return

    database = database_search("groups", "chat_id", chat.id)
    if database[0] == False:
        await Message.edit_message(update, database[1], sent_msg)
        return
    
    find_group = database[1]
    
    filters = find_group.get("filters")

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
    
    await Message.edit_message(update, f"<code>{msg_keywords}</code> has been added as filter!\n<b>Admin:</b> {user.first_name}", sent_msg)
