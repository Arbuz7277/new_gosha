import logging

logger = logging.getLogger(__name__)

def register(bot):
    @bot.message_handler(commands=['start'])
    def start(msg):
        bot.send_message(msg.chat.id, "Hello!")

        logger.info(f"Command /start from {msg.from_user.id}")