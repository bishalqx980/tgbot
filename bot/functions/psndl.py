from telegram import Update
from telegram.ext import ContextTypes
from bot.helper.telegram_helper import Message
from bot.modules.psndl import PSNDL
from bot.modules.telegraph import TELEGRAPH


async def func_psndl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyword = " ".join(context.args)

    if not keyword:
        await Message.reply_message(update, "Use <code>/psndl game name</code>\nE.g. <code>/psndl grand theft auto</code>")
        return

    if len(keyword) < 5:
        await Message.reply_message(update, "Search keyword is too short...")
        return

    sent_msg = await Message.reply_message(update, f"Searching...")
    search = await PSNDL.search(keyword)

    if not search:
        await Message.edit_message(update, "Game not found! Check game name again!", sent_msg)
        return

    msg_list, counter = [], 0
    for game_type in search:
        collections = search.get(game_type)
        for game_id in collections:
            game_data = collections.get(game_id)
            counter += 1
            msg_list.append(
                f"<b>No. {counter}</b>\n"
                f"<b>• ID:</b> <code>{game_data.get('id')}</code>\n"
                f"<b>• Name:</b> <code>{game_data.get('name')}</code>\n"
                f"<b>• Type:</b> <code>{game_data.get('type')}</code>\n"
                f"<b>• Region:</b> <code>{game_data.get('region')}</code>\n"
                f"<b>• Link:</b> <a href='{game_data.get('link')}'>Download</a>\n"
                f"<b>• Rap:</b> <code>{game_data.get('rap_name')}</code>\n"
                f"<b>• Rap data »</b> <code>/rap {game_data.get('rap_data')}</code>\n"
                f"<b>• Desc:</b> <code>{game_data.get('desc')}</code>\n"
                f"<b>• Author:</b> <code>{game_data.get('author')}</code>\n\n"
                "<i><b>Note:</b> To get rap file send the rap data with command /rap</i>\n\n"
            )
    
    msg, counter, links = "", 0, []
    for one_msg in msg_list:
        msg += one_msg.replace("\n", "<br>")
        counter += 1
        if len(msg_list) > 50 and counter == 50:
            link = await TELEGRAPH.paste(msg, f"{user.full_name} | {user.id}")
            links.append(link)
            msg, counter = "", 0
    
    if counter != 0:
        link = await TELEGRAPH.paste(msg, f"{user.full_name} | {user.id}")
        links.append(link)
        msg, counter = "", 0
    
    for link in links:
        msg += f"» {link}\n"
    await Message.edit_message(update, msg, sent_msg)


async def func_rap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    rap_data = " ".join(context.args)

    if not rap_data:
        await Message.reply_message(update, "Use <code>/rap rap_data</code>\nE.g. <code>/rap D78710F4C0979FAD9CDB40C612C94F60</code>\n<i><b>Note:</b> You will get the rap data after searching content/game using /psndl command.</i>")
        return

    sent_msg = await Message.reply_message(update, "Creating...")

    gen_rap = await PSNDL.gen_rap(rap_data)
    if not gen_rap:
        await Message.edit_message(update, "RAP file wasn't found!", sent_msg)
        return
    
    game_data, rap_name, rap_location = gen_rap
    rap_file = open(rap_location, "rb").read()

    caption = (
        f"<b>• ID:</b> <code>{game_data.get('id')}</code>\n"
        f"<b>• Name:</b> <code>{game_data.get('name')}</code>\n"
        f"<b>• Type:</b> <code>{game_data.get('type')}</code>\n"
        f"<b>• Region:</b> <code>{game_data.get('region')}</code>\n"
    )

    await Message.send_document(chat.id, rap_file, rap_name, caption)
    await Message.delete_message(chat.id, sent_msg)
