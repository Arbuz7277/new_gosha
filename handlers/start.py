# start.py
from aiogram import Router, types
from aiogram.filters import Command
from database.db_manager import db
from services.user import User

router = Router()

@router.message(Command("start"))
async def start(msg: types.Message):
    user = User(msg.from_user)
    await user.update()
    await msg.answer(f"Салам, {user.data.name}!\n\nВаш баланс: {user.data.balance / 100}\nВаш айди: {user.data.id}")

