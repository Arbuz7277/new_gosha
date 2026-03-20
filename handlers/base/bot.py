import logging

logger = logging.getLogger(__name__)

def register(bot):
    @bot.message_handler(comamnds=['bot'])
    def echo_bot(msg):
        msg.send_message(msg.chat.id, "Im here!")

        logger.info(f"Command /bot from {msg.from_user.id}")