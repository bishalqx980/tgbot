from telegram import Message, User
from bot import TL_LANG_CODES_URL
from bot.helpers import BuildKeyboard
from bot.modules.translator import translate

async def autoTranslate(message: Message, user: User, lang_code: str):
    """
    :param message: `update.message`
    :param user: `update.effective_user`
    :param lang_code: Get from user/chat database
    """
    text = message.text or message.caption
    # main func
    response = translate(text, lang_code)

    if response is False:
        btn = BuildKeyboard.ubutton([{"Language code's": TL_LANG_CODES_URL}])
        await message.reply_text("Invalid language code was given! Use /settings to set chat language.", reply_markup=btn)
        return
    
    if response.lower() != text.lower():
        await message.reply_text(f"{user.mention_html()}: {response}")
