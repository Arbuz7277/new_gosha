import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from database.db_manager import db

logger = logging.getLogger(__name__)


@dataclass
class UserData:
    id: int
    telegram_id: int
    name: str
    balance: int
    created_at: datetime

class User:
    def __init__(self, from_user):
        self.from_user = from_user
        self.data: Optional[UserData] = None

    async def update(self):
        row_data = await db.get_user(self.from_user)
        self.data = UserData(**row_data)
        return True
