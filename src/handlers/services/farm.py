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
    @bot.message_handler(commands=['farm', 'фарм'])
    def farm(msg):
        logger.info(f"Command /farm from {msg.from_user.id}")

        user = User(msg.from_user)

        total_s = time.time() - user.last_farm
        if total_s < cfg.farm_cooldown_seconds:
            days = int(total_s // 86400)
            hours = int((total_s % 86400) // 3600)
            minutes = int((total_s % 3600) // 60)
            seconds = int((total_s % 60) // 1)

            text = f"❌ <b>Рано!</b>\n\n<a href='tg://user?id={user.telegram_id}'>⏳</a> До фармы осталось"
            text += f"{days} дн." if days else ''
            text += f"{hours} ч." if hours else ''
            text += f"{minutes} мин." if minutes else ''
            text += f"{seconds} сек." if seconds else ''

            logger.info(f"The {msg.from_user.id}'s coldown has not passed.")
            msg.send_message(msg.chat.id, text, parse_mode='HTML')
            return

        random_money = random.randint(cfg.random_range_farm[0], cfg.random_range_farm[1])
        bank.create_check(
            amount=random_money,
            commision_precent=0,
            sender=0,
            recipient=user.id,
            type=cfg.FARM
        )
        user.update()

        text = f"<a href='tg://user?id={msg.from_user.id}'>✅</a> <b>Успешно!</b>\n\n"
        text += f"Вы нафармили {cent_to_coin(random_money)} коинов.\n"
        text += f"Ваш баланс: {user.balance}"

        bot.send_message(msg.chat.id, text, parse_mode='HTML')