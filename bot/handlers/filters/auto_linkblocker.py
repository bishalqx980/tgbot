from telegram import Message, User
from bot.modules.re_link import RE_LINK
from bot.modules.base64 import BASE64

async def autoLinkBlocker(message: Message, user: User, link_rules: dict):
    """
    :param message: `update.message`
    :param user: `update.effective_user`
    :param link_rules: `dict` of link rules (database variables)
    """
    links_behave = link_rules.get("links_behave") # 3 values: delete; convert; None;
    allowed_links = link_rules.get("allowed_links") or []
    # filtering links
    filtered_allowed_links = []
    for link in allowed_links:
        filtered_allowed_links.append(RE_LINK.extractDomainName(link.strip()))
    allowed_links = filtered_allowed_links

    text = message.text or message.caption
    # main func
    links = RE_LINK.detectLinks(text)
    if not links:
        return
    
    counter = 0
    for link in links:
        domain = RE_LINK.extractDomainName(link)

        if domain in allowed_links:
            counter += 1
        
        else:
            if links_behave == "delete":
                text = text.replace(link, f"<code>forbidden link</code>")
            
            elif links_behave == "convert":
                text = text.replace(link, f"<code>{BASE64.encode(link)}</code>")

    if counter != len(links):
        await message.delete()
        text = (
            f"{user.mention_html()}: {text}\n\n"
            "<i>Delete reason: your message contains forbidden link/s!</i>"
        )
        await message.reply_text(text)
        return text
