from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from ... import logger
from ...helper.button_maker import ButtonMaker
from ...modules.database import MemoryDB

async def query_chat_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    query = update.callback_query

    # refined query data
    query_data = query.data.removeprefix("csettings_")

    # memory access
    data_center = MemoryDB.data_center.get(chat.id) # ChatID bcz its for both Private & Public Chat
    if not data_center:
        await query.answer("Session Expired.", True)
        try:
            message_id = query.message.message_id
            await context.bot.delete_messages(chat.id, [message_id, message_id - 1])
        except:
            try:
                await query.delete_message()
            except:
                pass
        return
    
    # verifying user
    user_id = data_center.get("user_id")
    if user_id != user.id:
        await query.answer("Access Denied!", True)
        return
    
    # common variable for chat_data and user_data
    memory_data = MemoryDB.chat_data.get(chat.id) or MemoryDB.user_data.get(chat.id)

    # variable required for global reply
    is_editing_btn = None
    is_boolean_btn = None

    if query_data == "menu":
        # Handling PRIVATE chat setting
        if chat.type == ChatType.PRIVATE:
            text = (
                "<blockquote><b>Chat Settings</b></blockquote>\n\n"

                f"• Name: {user.mention_html()}\n"
                f"• ID: <code>{user.id}</code>\n\n"

                f"• Language: <code>{memory_data.get('lang')}</code>\n"
                f"• Auto translate: <code>{memory_data.get('auto_tr') or False}</code>\n"
                f"• Echo: <code>{memory_data.get('echo') or False}</code>"
            )

            btn_data = [
                {"Language": "csettings_lang", "Auto translate": "csettings_auto_tr"},
                {"Echo": "csettings_echo", "Close": "csettings_close"}
            ]

            btn = ButtonMaker.cbutton(btn_data)
        
        else:
            text = (
                "<blockquote><b>Chat Settings</b></blockquote>\n\n"

                f"• Title: {chat.title}\n"
                f"• ID: <code>{chat.id}</code>\n\n"

                f"• Language: <code>{memory_data.get('lang')}</code>\n"
                f"• Auto translate: <code>{memory_data.get('auto_tr') or False}</code>\n"
                f"• Echo: <code>{memory_data.get('echo') or False}</code>\n"
                f"• Antibot: <code>{memory_data.get('antibot') or False}</code>\n"
                f"• Welcome Members: <code>{memory_data.get('welcome_user') or False}</code>\n"
                f"• Farewell Members: <code>{memory_data.get('farewell_user') or False}</code>\n"
                f"• Join Request: <code>{memory_data.get('chat_join_req')}</code>\n"
                f"• Service Messages: <code>{memory_data.get('service_messages')}</code>\n"
                f"• Links Behave: <code>{memory_data.get('links_behave')}</code>\n"
                f"• Allowed Links: <code>{', '.join(memory_data.get('allowed_links') or [])}</code>"
            )

            btn_data = [
                {"Language": "csettings_lang", "Auto translate": "csettings_auto_tr"},
                {"Echo": "csettings_echo", "Antibot": "csettings_antibot"},
                {"Welcome Members": "csettings_welcome_user", "Farewell Members": "csettings_farewell_user"},
                {"Links Behave": "csettings_links_behave", "Allowed Links": "csettings_allowed_links"},
                {"Join Request": "csettings_chat_join_req", "Service Messages": "csettings_service_messages"},
                {"Close": "csettings_close"}
            ]

            btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "lang":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "lang",
            "is_list": False,
            "is_int": False
        })

        is_editing_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Language: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> <a href='{}'>Available language codes</a>\nExample: <code>en</code> for English language.</blockquote>"
        ).format(memory_data.get("lang"), "https://telegra.ph/Language-Code-12-24")
    
    elif query_data == "auto_tr":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "auto_tr",
            "is_list": False,
            "is_int": False
        })

        is_boolean_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Auto translate: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will automatically translate chat messages to seleted language.</blockquote>"
        ).format(memory_data.get("auto_tr") or False)
    
    elif query_data == "echo":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "echo",
            "is_list": False,
            "is_int": False
        })

        is_boolean_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Echo: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will echo user messages.</blockquote>"
        ).format(memory_data.get("echo") or False)
    
    elif query_data == "antibot":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "antibot",
            "is_list": False,
            "is_int": False
        })

        is_boolean_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Antibot: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> If someone try to add bots in chat, this will kick the bot, if enabled.</blockquote>"
        ).format(memory_data.get("antibot"))
    
    elif query_data == "welcome_user":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "welcome_user",
            "is_list": False,
            "is_int": False
        })

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Welcome Members: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will welcome new chat member, if enabled.</blockquote>"
        ).format(memory_data.get("welcome_user") or False)

        btn_data = [
            {"Enable": "database_bool_true", "Disable": "database_bool_false"},
            {"Custom Welcome Message": "csettings_custom_welcome_msg"},
            {"Back": "csettings_menu", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "custom_welcome_msg":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "custom_welcome_msg",
            "is_list": False,
            "is_int": False
        })

        custom_message = memory_data.get("custom_welcome_msg") or ""

        if len(custom_message) > 500:
            await context.bot.send_message(chat.id, f"Custom Greeting Message:\n\n{custom_message}")
            custom_message = "Message is too long."
        
        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Custom Welcome Message:\n<code>{}</code>\n"
            "<blockquote><b>Note:</b> Custom welcome message to greet new chat members. (supports telegram formatting)</blockquote>"
        ).format(custom_message)

        btn_data = [
            {"Set Custom Message": "database_edit_value", "Remove Custom Message": "database_rm_value"},
            {"Formattings": "csettings_formattings"},
            {"Back": "csettings_welcome_user", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "formattings":
        text = (
            "<blockquote><b>Formattings</b></blockquote>\n\n"
            "• <code>{first}</code> - users firstname\n"
            "• <code>{last}</code> - users lastname\n"
            "• <code>{fullname}</code> - users fullname\n"
            "• <code>{username}</code> - users username\n"
            "• <code>{mention}</code> - mention user\n"
            "• <code>{id}</code> - users ID\n"
            "• <code>{chatname}</code> - chat title"
        )

        btn = ButtonMaker.cbutton([{"Back": "csettings_custom_welcome_msg", "Close": "csettings_close"}])
    
    elif query_data == "farewell_user":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "farewell_user",
            "is_list": False,
            "is_int": False
        })

        is_boolean_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Farewell Members: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will send a farewell message to chat when a member left, if enabled.</blockquote>"
        ).format(memory_data.get("farewell_user"))
    
    elif query_data == "chat_join_req":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "chat_join_req",
            "is_list": False,
            "is_int": False
        })

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Join Request: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will auto Approve or Decline or Do Nothing while a member request to join this Group. (Bot should have add/invite member permission.)</blockquote>"
        ).format(memory_data.get("chat_join_req"))

        btn_data = [
            {"Approve": "database_value_approve", "Decline": "database_value_decline", "Do Nothing": "database_rm_value"},
            {"Back": "csettings_menu", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "service_messages":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "service_messages",
            "is_list": False,
            "is_int": False
        })

        is_boolean_btn = True
        
        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Service Messages: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> This will auto delete chat service messages (new member join, chat photo update etc.)</blockquote>"
        ).format(memory_data.get("service_messages"))
    
    elif query_data == "links_behave":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "links_behave",
            "is_list": False,
            "is_int": False
        })

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Links Behave: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> Links has 3 behaves: [ Delete / Convert to base64 / Do Nothing ]\n"
            "The Links Behave action will be triggered if any non-admin member shares a link in the chat.</blockquote>"
        ).format(memory_data.get("links_behave"))

        btn_data = [
            {"Delete": "database_value_delete", "Convert to base64": "database_value_convert", "Do Nothing": "database_rm_value"},
            {"Back": "csettings_menu", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data)
    
    elif query_data == "allowed_links":
        MemoryDB.insert("data_center", chat.id, {
            "update_data_key": "allowed_links",
            "is_list": True,
            "is_int": False
        })

        is_editing_btn = True

        text = (
            "<blockquote><b>Chat Settings</b></blockquote>\n\n"
            "Allowed links: <code>{}</code>\n\n"
            "<blockquote><b>Note:</b> Send domain name of allowed links. Example: <code>google.com</code> ! Multiple domain should be separated by comma."
            "Allowed links won't be affected by <code>Links Behave</code></blockquote>"
        ).format(", ".join(memory_data.get("allowed_links") or []))
    
    elif query_data == "close":
        try:
            message_id = query.message.message_id
            await context.bot.delete_messages(chat.id, [message_id, message_id - 1])
        except:
            try:
                await query.delete_message()
            except:
                pass
        return # don't want to edit message by global reply
    
    # common editing keyboard buttons
    if is_editing_btn:
        btn_data = [
            {"Edit Value": "database_edit_value"},
            {"Remove Value": "database_rm_value"},
            {"Back": "csettings_menu", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data) # cant use btn as common bcz maybe there are other btn
    
    if is_boolean_btn:
        btn_data = [
            {"Enable": "database_bool_true", "Disable": "database_bool_false"},
            {"Back": "csettings_menu", "Close": "csettings_close"}
        ]

        btn = ButtonMaker.cbutton(btn_data) # cant use btn as common bcz maybe there are other btn
    
    # global reply
    try:
        await query.edit_message_caption(text, reply_markup=btn)
    except BadRequest:
        await query.edit_message_text(text, reply_markup=btn)
    except Exception as e:
        logger.error(e)
