from app import logger, config
from app.database import MongoDB


def update_database(force_update: bool = False):
    logger.info("Updating settings on database...")

    if not force_update:
        bot_data = MongoDB.get_bot_data()
        if bot_data:
            message = "Settings are already updated on database. Skiping update process!"
            logger.info(message)
            return message

    config_data = vars(config)

    update = MongoDB.insert(
        MongoDB.SETTINGS,
        data = config_data
    )

    if update:
        message = "Settings are updated on database."
        logger.info(message)
        return message
