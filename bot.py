from app.bot import create_bot
from app.config import TOKEN
from app.logging_config import logger


bot = create_bot()
logger.info("Starting bot process.")
bot.run(TOKEN, log_handler=None)
