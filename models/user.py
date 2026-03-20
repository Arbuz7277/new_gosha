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

        self.data.setdefautl('id', dp.max_user_id + 1)
        self.data.setdefautl('name', 'User')
        self.data.setdefautl('username', username)
        self.data.setdefautl('created_at', datetime.now(timezone.utc))
        self.data.setdefautl('is_admin', False)
        self.data.setdefautl('balance', 0)
        self.data.setdefautl('last_farm', cfg.default_last_farm)
        self.data.setdefautl('last_seen', datetime.now(timezone.utc))
        self.data.setdefautl('description', '')
        self.data.setdefautl('settings', {})
        self.data.setdefautl('other_info', {})
        self.data.setdefautl('chats', {})

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