import os
import json
from dotenv import load_dotenv
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

load_dotenv()


class Config:
    def __init__(self):
        self.token = os.getenv('API_KEY')

        if not self.token:
            raise ValueError("API_KEY not found in .env file!")

        # === Paths ===
        self.dp_path = Path('database')
        if not os.path.exists(self.dp_path): os.mkdir(self.dp_path)

        self.json_users_path = self.dp_path / 'users.json'
        if not os.path.exists(self.json_users_path):
            with open(self.json_users_path, 'w') as f:
                json.dump({}, f)

        self.json_bank_path = self.dp_path / 'bank.json'
        if not os.path.exists(self.json_bank_path):
            with open(self.json_bank_path, 'w') as f:
                json.dump({"max_check_id": 0, "transfers": {}}, f)


        # Values
        self.max_len_name = 16
        self.min_len_name = 3
        self.min_len_description_user = 1
        self.max_len_description_user = 255
        self.farm_cooldown_seconds = 60
        self.char_money = '¢'
        self.len_check_key = 48
        self.chars_check_key = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!$^&*-"
        self.random_range_farm = (100, 1000)

        # Transfer Type
        self.TRANSFER = "TRANSFER"
        self.FARM = "FARM"
        self.ADMIN = "ADMIN"
        self.GAME = "GAME"

    @property
    def default_last_farm(self):
        return 0