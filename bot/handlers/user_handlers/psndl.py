from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.psndl_module import PSNDL
from bot.modules import telegraph

async def func_psndl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    effective_message = update.effective_message
    game_name = " ".join(context.args)

    if not game_name:
        await effective_message.reply_text(
            "Use <code>/psndl game name</code>\n"
            "E.g. <code>/psndl red dead redemption</code>\n\n"
            "PSNDL Website: https://bishalqx980.github.io/psndl/"
        )
        return

    if len(effective_message.text) < 4:
        await effective_message.reply_text("Search keyword is too short...")
        return

    sent_message = await effective_message.reply_text(f"Searching...")

    result = await PSNDL.search(game_name)
    response = {
        404: "Error: fetching database!",
        500: "Package wasn't found! Check package name again!",
        None: "Oops! Something went wrong!"
    }

    if type(result) is not dict and result in response:
        await sent_message.edit_text(response[result])
        return
    
    msg_list, counter = [], 0
    for game_type in result:
        collections = result.get(game_type)
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
                "<blockquote><b>Note:</b> To get rap file send the rap data with command /rap</blockquote>\n\n"
            )
    
    msg, counter, links = "", 0, []
    for one_msg in msg_list:
        msg += one_msg.replace("\n", "<br>")
        counter += 1
        if len(msg_list) > 50 and counter == 50:
            link = await telegraph.paste(msg, f"{user.full_name} | {user.id}")
            links.append(link if link else "Missing link!")
            msg, counter = "", 0
    
    if counter != 0:
        link = await telegraph.paste(msg, f"{user.full_name} | {user.id}")
        links.append(link if link else "Missing link!")
        msg, counter = "", 0
    
    for link in links:
        msg += f"• {link}\n"

    await sent_message.edit_text(f"{msg}\nPSNDL Website: https://bishalqx980.github.io/psndl/")
