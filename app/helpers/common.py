from app import bot, logger, COMMAND_PREFIXES


def _version_compare(current, latest):
    return tuple(map(int, current.split("."))) >= tuple(map(int, latest.split(".")))


def CommandArgs(text: str, commands: list, prefixes: list = COMMAND_PREFIXES):
    """
    Extracts args from given text by removing command & prefixes.
    
    :param text: the text to get args from
    :param commands: list of command names
    :param prefixes: list of command prefixes
    :return: stripped text after removing command and prefix
    """
    try:
        for p in prefixes:
            if text.startswith(p):
                text = text[len(p):]
                break
        
        for c in commands:
            if text.startswith(c):
                text = text[len(c):]
                break

        # remove /command@bot_username
        username = f"@{bot.me.username}"

        if text.startswith(username):
            text = text[len(username):]

        return text.strip()
    except Exception as e:
        logger.error(e)
