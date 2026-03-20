import logging
import models.user

logger = logging.getLogger(__name__)

def register(bot):
    @bot.message_handler(commands=['start'])
    def start(msg):
        user = models.user.User(msg.from_user.id, msg.from_user.username)
        bot.send_message(msg.chat.id, "Твой профиль:"
                                      f"Имя: {user.data['name']}"
                                      f"Дата регистрации: {user.data['created_at']}"
                                      f"Баланс: {user.balance}")

        logger.info(f"Command /start from {msg.from_user.id}")