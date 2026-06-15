import logging
import aiosqlite
from pathlib import Path
import asyncio
from typing import List, Optional, Tuple, Any
from config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    # Управление базой данных
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Config.db_path

        self.db_path = str(db_path)

    async def _init_tables(self):
        # Инициализация всех таблиц
        async with aiosqlite.connect(self.db_path) as conn:
            # Таблица пользователей
            # balance - хранится в центах
            async with conn.execute("CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "telegram_id INTEGER NOT NULL CHECK (telegram_id BETWEEN 1000000000 AND 9999999999),"
                "name TEXT NOT NULL DEFAULT 'User',"
                "balance INTEGER NOT NULL DEFAULT 0,"
                "last_farm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                "last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                ")") as cursor:
                    await conn.commit()

            # Таблица банка
            """
            amount_sent - отправленное кол-во центов
            fee - комиссия в центах
            amount_received - полученное кол-во центов
            fee_percent - процент комиссии в десятичной дроби
            """
            async with conn.execute("CREATE TABLE IF NOT EXISTS bank ("
                "id BLOB PRIMARY KEY,"
                "sender INT,"
                "recipient INT NOT NULL,"
                "amount_sent INT NOT NULL,"
                "fee INT NOT NULL,"
                "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                "amount_received INT GENERATED ALWAYS AS (amount_sent - fee) STORED,"
                "fee_percent REAL GENERATED ALWAYS AS (CAST(fee AS REAL) / amount_sent) STORED"
                ")") as cursor:
                    await conn.commit()

        logger.info("DatabaseManager initializated")

    async def execute(self, sql: str, params: tuple = ()) -> aiosqlite.Cursor:
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute(sql, params) as cursor:
                await conn.commit()
                return cursor

    async def fetch_one(self, sql: str, params: tuple = ()) -> Optional[Tuple]:
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute(sql, params) as cursor:
                await conn.commit()
                return await cursor.fetchone()

    async def fetch_all(self, sql: str, params: tuple = ()) -> List[Tuple]:
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute(sql, params) as cursor:
                await conn.commit()
                return await cursor.fetchall()

    async def get_user(self, from_user) -> tuple:
        row_data = await self.fetch_one("SELECT * FROM users WHERE telegram_id = ?", (from_user.id,))
        if not row_data:
            await self.execute("INSERT INTO users (telegram_id) VALUES (?)", (from_user.id,))
            row_data = await self.fetch_one("SELECT * FROM users WHERE telegram_id = ?", (from_user.id,))
            logger.info(f"User {from_user.id} was register")
        
        return row_data

        
async def init():
    db = DatabaseManager()
    await db._init_tables()
    return db

db = asyncio.run(init())
