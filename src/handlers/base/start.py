import logging
from src.models.user import User
from src.config import Config

logger = logging.getLogger(__name__)
cfg = Config()

def register(bot):
    @bot.message_handler(commands=['start'])
    def start(msg):
        user = User(msg.from_user)
        bot.send_message(msg.chat.id, "Твой профиль:\n\n"
                                      f"Имя: {user.name}\n"
                                      f"Дата регистрации: {user.data['created_at']}\n"
                                      f"Баланс: {user.balance} {cfg.char_money}")

        logger.info(f"Command /start from {msg.from_user.id}")