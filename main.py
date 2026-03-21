import time
import os
import logging
import telebot
from src.models.bot import Bot
from src.config import Config

def setup_logging():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s : <%(name)s> : %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/bot.log', encoding='utf-8')
        ]
    )

    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('telebot').setLevel(logging.WARNING)

def main():
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("Bot running...")

    config = Config()
    bot = Bot(config.token)
    bot.register_handlers()
    bot.run()

if __name__ == '__main__':
    main()