import logging
import time
import random

from src.models.user import User
from src.models.bank import Bank
from src.config import Config
from src.utils.base import cent_to_coin

logger = logging.getLogger(__name__)
bank = Bank()
cfg = Config()

def register(bot):
    @bot.message_handler(commands=['check', 'чек'])
    def check(msg):
        logger.info(f"Command /check from {msg.from_user.id}")

        user = User(msg.from_user)

        args = msg.text.split(' ', 2)[1:]
        check_id = args[0] if len(args) > 0 else None
        check_key = args[1] if len(args) > 1 else None

        check = bank.get_check(check_id, user.id, check_key)
        if not check:
            bot.reply_to(msg, "❌ <b>Доступ запрещен</b>", parse_mode='HTML')
            return

        text = f"📄 <b>Чек №{check['id']}</b>\n\n"

        text += f"Айди: {check['id']}\n"
        text += f"Создание: {check['created_at']}\n"
        text += f"Сумма: {check['amount']}\n"
        text += f"Комиссия (процент): {check['commission_precent']}\n"
        text += f"Комиссия (сумма): {check['commission_money']}\n"
        text += f"Переведено: {check['received']}\n"
        text += f"Отправитель (id): {check['sender']}\n"
        text += f"Получатель (id): {check['recipient']}\n"
        text += f"Тип: {check['type']}\n"
        text += f"Описание: {check['description']}\n"
        text += f"Ключ: <tg-spoiler>{check['key']}</tg-spoiler>\n"

        bot.send_message(msg.from_user.id, text, parse_mode='HTML')