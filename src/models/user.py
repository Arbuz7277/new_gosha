import time
from datetime import datetime, timezone

from .database import Database
from .. import config

cfg = config.Config()
dp = Database()

class User:
    def __init__(self, uid: int, username: str = None):
        self.telegram_id = uid

        users = dp.load_users()
        self.data = users.setdefault(str(self.telegram_id), {})

        self.data.setdefault('id', dp.max_user_id + 1)
        self.data.setdefault('name', 'User')
        self.data.setdefault('username', username)
        self.data.setdefault('created_at', f"{datetime.now(timezone.utc)}")
        self.data.setdefault('is_admin', False)
        self.data.setdefault('balance', 0)
        self.data.setdefault('last_farm', cfg.default_last_farm)
        self.data.setdefault('last_seen', f"{datetime.now(timezone.utc)}")
        self.data.setdefault('description', '')
        self.data.setdefault('settings', {})
        self.data.setdefault('other_info', {})
        self.data.setdefault('chats', {})

        self.save()

    @property
    def balance(self):
        return round(self.balance / 100, 2)

    @balance.setter
    def set_balance(self, value):
        if value < 0:
            value = 0

        self.balance = value
        self.save()

    def save(self):
        dp.save_user(self.data)