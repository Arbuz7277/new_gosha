import logging
import time
import random
from itertools import chain

from src.models.user import User
from src.models.bank import Bank
from src.config import Config
from src.utils.base import cent_to_coin

logger = logging.getLogger(__name__)
bank = Bank()
cfg = Config()

# reduce_to_five

def register(bot):
    @bot.message_handler(commands=['farm', 'фарм'])
    def farm(msg):
        logger.info(f"Command /farm from {msg.from_user.id}")

        user = User(msg.from_user)

        passed_s = time.time() - user.last_farm
        if passed_s < cfg.farm_cooldown_seconds:
            total_s = cfg.farm_cooldown_seconds - passed_s
            days = int(total_s // 86400)
            hours = int((total_s % 86400) // 3600)
            minutes = int((total_s % 3600) // 60)
            seconds = int((total_s % 60) // 1)

            text = f"❌ <b>Рано!</b>\n\n<a href='tg://user?id={user.telegram_id}'>⏳</a> До фармы осталось"
            text += f" {days} дн." if days else ''
            text += f" {hours} ч." if hours else ''
            text += f" {minutes} мин." if minutes else ''
            text += f" {seconds} сек." if seconds else ''

            logger.warning(f"The {msg.from_user.id}'s coldown has not passed.")
            bot.send_message(msg.chat.id, text, parse_mode='HTML')
            logger.debug(f"Send message to {msg.chat.id}")
            return

        random_money = random.randint(cfg.random_range_farm[0], cfg.random_range_farm[1])
        check = bank.create_check(
            amount=random_money,
            commision_precent=0,
            sender=0,
            recipient=user.id,
            type=cfg.FARM
        )
        user.set_last_farm()
        user.update()

        text = f"✅ <b>Успешно!</b>\n\n"
        text += f"<a href='tg://user?id={msg.from_user.id}'>Вы</a> нафармили {cent_to_coin(check['received'])} {cfg.char_money}.\n"
        text += f"Ваш баланс: {user.balance} {cfg.char_money}"

        bot.send_message(msg.chat.id, text, parse_mode='HTML')
        logger.debug(f"Send message to {msg.chat.id}")