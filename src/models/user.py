import time
from datetime import datetime, timezone

from .database import Database
from .. import config

cfg = config.Config()
dp = Database()

class User:
    def __init__(self, tg):
        self.data_update = True

        self.__tg = tg

        users = dp.load_users()
        uid = []
        for user in users.values():
            if user['telegram_id'] == tg.id:
                uid.append(user['id'])


        if not uid:
            self.data = users.setdefault(str(dp.max_user_id + 1), {})
            self.data.setdefault('id', dp.max_user_id + 1)
        else:
            self.data = users[str(uid[0])]
            self.data.setdefault('id', uid[0])
        self.data.setdefault('telegram_id', tg.id)
        self.data.setdefault('name', tg.first_name)
        self.data.setdefault('username', tg.username)
        self.data.setdefault('created_at', f"{datetime.now(timezone.utc)}")
        self.data.setdefault('is_admin', False)
        self.data.setdefault('balance', 0)
        self.data.setdefault('last_farm', cfg.default_last_farm)
        self.data['last_seen'] = f"{datetime.now(timezone.utc)}"
        self.data.setdefault('description', '')
        self.data.setdefault('settings', {})
        self.data.setdefault('other_info', {})
        self.data.setdefault('chats', {})

        if self.data['username'] != tg.username:
            self.data['username'] = tg.username



        self.save()

    # === Name ===
    @property
    def name(self):
        return self.data['name']
    @name.setter
    def set_name(self, name):
        if not isinstance(name, str):
            raise TypeError(f"argument 'name' must be str, got {type(name).__name__}")

        last_name = self.data['name']
        self.data['name'] = name

        if last_name != name: self.data_update = True
        self.save()
    @name.deleter
    def delete_name(self):
        self.data['name'] = "User"
        self.save()

    # === Balance ===
    @property
    def balance(self):
        return round(self.data['balance'] / 100, 2)

    # === Description ===
    @property
    def description(self):
        return self.data['description']
    @description.setter
    def set_description(self, new_description):
        if not isinstance(new_description, str):
            raise TypeError(f"argument 'money' must be str, got {type(name).__name__}")

        last_description = self.date['description']
        self.date['description'] = new_description

        if last_description != new_description:
            self.data_update = True
        self.save()
    @description.deleter
    def delete_description(self):
        last_description = self.data['description']
        self.data['description'] = None
        if last_description != self.data['description']:
            self.data_update = True
        self.save()

    # == Last Farm ===
    @property
    def last_farm(self):
        return self.data['last_farm']

    # === Telegram ID ===
    @property
    def telegram_id(self):
        return self.data['telegram_id']

    # === ID ===
    @property
    def id(self):
        return self.data['id']


    def set_last_farm(self):
        self.data['last_farm'] = time.time()
        self.data_update = True
        self.save()

    def set_admin(self):
        if not self.data['is_admin']:
            self.data['is_admin'] = True
        else:
            self.data['is_admin'] = False
        self.data_update = True
        self.save()

    def save(self):
        if self.data_update:
            self.data_update = False
            dp.save_user(self.data)

    def update(self):
        self.__init__(self.__tg)