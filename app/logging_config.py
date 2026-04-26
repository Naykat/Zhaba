import logging


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup_logging():
    formatter = logging.Formatter(LOG_FORMAT)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.WARNING)

    app_logger = logging.getLogger("reaction_roles_bot")
    app_logger.handlers.clear()
    app_logger.setLevel(logging.INFO)
    app_logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    app_logger.addHandler(console_handler)

    for logger_name in ("discord", "discord.client", "discord.gateway", "discord.http"):
        discord_logger = logging.getLogger(logger_name)
        discord_logger.handlers.clear()
        discord_logger.propagate = False
        discord_logger.disabled = True

    return app_logger


logger = setup_logging()
