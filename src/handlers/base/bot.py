import logging

logger = logging.getLogger(__name__)

def register(bot):
    @bot.message_handler(comamnds=['bot'])
    def echo_bot(msg):
        bot.reply_to(msg, "Im here!")

        logger.info(f"Command /bot from {msg.from_user.id}")