# farm.py
import random
from datetime import datetime, timedelta, timezone
from aiogram import Router, types
from aiogram.filters import Command
from services.user import User
from services.bank import bank
from config import Config

router = Router()

def can_farm(last_farm: datetime) -> bool:
    """Проверяет кулдаун фарма"""
    now = datetime.now(timezone.utc)
    time_passed = now - last_farm
    return time_passed >= timedelta(seconds=Config.farm.cooldown)

def get_passed_time_farm(last_farm: datetime) -> tuple:
    """
    :param last_farm: последний фарм
    :return: (days, hours, minutes, seconds)
    """
    now = datetime.now(timezone.utc)
    time_passed = now - last_farm
    total_seconds = int(time_passed.total_seconds())

    # Разбираем
    days = int(total_seconds // 86400)
    hours = int((total_seconds % 86400) // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    return (days, hours, minutes, seconds)

@router.message(Command("farm"))
async def start(msg: types.Message):
    user = User(msg.from_user)
    await user.update()

    # Если не прошел кулдаун
    if not can_farm(user.data.last_farm):
        # Получение данных об оставшемся времени
        passed = get_passed_time_farm(user.data.last_farm)
        await msg.answer(f"⏳ Подождите еще {passed[0]} дней, {passed[1]} часов, {passed[2]} минут и {passed[3]} секунд.")
        return

    # генерируем случайную награду
    reward = random.randint(Config.farm.min_value, Config.farm.max_value)

    # Выдаем пользователю
    await bank.add_money(user, reward)

    await msg.answer(f"✅ Вы нафармили {reward / 100} коинов!")