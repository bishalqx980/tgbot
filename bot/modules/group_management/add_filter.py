from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message, Button
from bot.modules.database.combined_db import global_search
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE
from bot.modules.group_management.pm_error import _pm_error
from bot.functions.del_command import func_del_command
from bot.modules.group_management.check_permission import _check_permission


async def func_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    e_msg = update.effective_message
    reply = update.message.reply_to_message
    value = reply.text_html or reply.caption if reply else None
    keyword = " ".join(context.args).lower()
    
    if chat.type not in ["group", "supergroup"]:
        await _pm_error(chat.id)
        return
    
    await func_del_command(update, context)

    if user.is_bot:
        await Message.reply_msg(update, "I don't take permission from anonymous admins!")
        return
    
    _chk_per = await _check_permission(update, user=user)

    if not _chk_per:
        return
    
    _bot_info, bot_permission, user_permission, admin_rights, victim_permission = _chk_per
        
    if bot_permission.status != ChatMember.ADMINISTRATOR:
        await Message.reply_msg(update, "I'm not an admin in this chat!")
        return
    
    if user_permission.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await Message.reply_msg(update, "You aren't an admin in this chat!")
        return
    
    if user_permission.status == ChatMember.ADMINISTRATOR:
        if not admin_rights.get("can_change_info"):
            await Message.reply_msg(update, "You don't have enough rights to manage this chat!")
            return
    
    if not value or not keyword:
        data = {
            "user_id": user.id,
            "chat_id": chat.id,
            "collection_name": None,
            "db_find ": None,
            "db_vlaue": None,
            "edit_data_key": None,
            "edit_data_value": None,
            "del_msg_pointer_id": e_msg.id,
            "edit_data_value_msg_pointer": None
        }

        await LOCAL_DATABASE.insert_data("data_center", chat.id, data)

        msg = (
            "To set filters for this chat follow the instruction below...\n"
            "<blockquote>Reply the message with /filter which one you want to set as value for your keyword!</blockquote>"
            "Example: <code>/filter hi</code> send this by replying any message! suppose the message is <code>Hi, How are you!</code>\n"
            "Next time if you say <code>Hi</code> in chat, the bot will reply with <code>Hi, How are you!</code>\n\n"
            "Ques: How to remove a filter?\n Ans: /remove for instruction..."
        )

        btn_name = ["Text formatting", "Close"]
        btn_data = ["text_formats", "close"]

        btn = await Button.cbutton(btn_name, btn_data, True)

        await Message.reply_msg(update, msg, btn)
        return

    db = await global_search("groups", "chat_id", chat.id)
    if db[0] == False:
        await Message.reply_msg(update, db[1])
        return
    
    find_group = db[1]
    
    filters = find_group.get("filters")
    if not filters:
        data = {
            keyword: value
        }
        await MongoDB.update_db("groups", "chat_id", chat.id, "filters", data)
    else:
        filters[keyword] = value
        await MongoDB.update_db("groups", "chat_id", chat.id, "filters", filters)
    
    group_data = await MongoDB.find_one("groups", "chat_id", chat.id)
    await LOCAL_DATABASE.insert_data("groups", chat.id, group_data)
    await Message.reply_msg(update, f"<code>{keyword}</code> has been added as filter!\n<b>Admin</b>: {user.first_name}")
