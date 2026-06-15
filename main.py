# main.py
import logging
from logging.handlers import RotatingFileHandler

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] : %(levelname)s %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            'bot.log',
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
    ]
)

import asyncio
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from handlers import main_router


logger = logging.getLogger(__name__)

load_dotenv()

token = os.getenv("API_KEY")

logger.info("Bot initialization")
bot = Bot(token=token)
dp = Dispatcher()

# Подключаем все роутеры из __init__.py
logger.info("Connecting handlers")
dp.include_router(main_router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
