import os
import json
from .. import config

cfg = config.Config()

class Database:
    def __init__(self):
        users = self.load_users()

        self.max_user_id = users.setdefault('max_id', 1)

    def inc_id(self, max_id: int = None):
        users = self.load_users()
        if max_id:
            self.max_user_id = max_id
            users['max_id'] = max_id
        else:
            self.max_user_id += 1
            users['max_id'] += 1
        self.save_users(users)

    def save_users(self, data):
        try:
            with open(cfg.json_users_path, 'w') as f:
                json.dump(data, f, indent=2)
                return True
        except Exception as e:
            raise Exception(f"Error in write to file {cfg.json_users_path}: {type(e).__name__}: {e}")

    def load_users(self):
        try:
            with open(cfg.json_users_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error in load file {cfg.json_users_path}: {type(e).__name__}: {e}")

    def save_user(self, data):
        uid = data['id']
        if uid > self.max_user_id:
            self.inc_id(uid)
        users = self.load_users()
        users[str(uid)] = data
        self.save_users(users)

    def load_user(self, uid):
        data = self.load_users()
        return data[str(uid)]

    def load_bank(self):
        try:
            with open(cfg.json_bank_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error in load file {cfg.json_bank_path}: {type(e).__name__}: {e}")

    def save_bank(self, data):
        try:
            with open(cfg.json_bank_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise Exception(f"Error in write to file {cfg.json_bank_path}: {type(e).__name__}: {e}")