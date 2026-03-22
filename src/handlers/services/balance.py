import logging

from src.models.user import User
from src.config import Config

logger = logging.getLogger(__name__)
cfg = Config()

def register(bot):
    @bot.message_handler(commands=['balance', 'money', 'баланс', 'бал'])
    def balance(msg):
        logger.info(f"command /balance from {msg.from_user.id}")
        user = User(msg.from_user)
        text = f"💰 <a href='tg://user?id={user.telegram_id}'>Ваш</a> баланс: {user.balance} {cfg.char_money}"
        bot.send_message(msg.chat.id, text, parse_mode='HTML')