from telegram import Update
from telegram.ext import ContextTypes
from bot.modules.psndl.psndl_func import PSNDL

async def func_rap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_message = update.effective_message
    hex_data = " ".join(context.args)

    if not hex_data:
        await effective_message.reply_text("Use <code>/rap rapData (hex)</code>\nE.g. <code>/rap D78710F4C0979FAD9CDB40C612C94F60</code>\n<blockquote><b>Note:</b> You will get the rap data after searching package using /psndl command.</blockquote>")
        return

    result = await PSNDL.gen_rap(hex_data)
    response = {
        404: "Error: fetching database!",
        500: "Package RAP wasn't found! Check HEX data again!",
        None: "Something went wrong!"
    }

    if type(result) is not dict and result in response:
        await effective_message.reply_text(response[result])
        return

    caption = (
        f"<b>• ID:</b> <code>{result['packageData'].get('id')}</code>\n"
        f"<b>• Name:</b> <code>{result['packageData'].get('name')}</code>\n"
        f"<b>• Type:</b> <code>{result['packageData'].get('type')}</code>\n"
        f"<b>• Region:</b> <code>{result['packageData'].get('region')}</code>\n"
    )

    await effective_message.reply_document(result["rapBytes"], caption)
