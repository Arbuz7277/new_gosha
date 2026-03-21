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

        self.dp_path = Path('database')
        if not os.path.exists(self.dp_path):
            os.mkdir(self.dp_path)

        self.json_users_path = self.dp_path / 'users.json'
        if not os.path.exists(self.json_users_path):
            with open(self.json_users_path, 'w') as f:
                json.dump({}, f)


        # Values
        self.max_len_name = 16
        self.min_len_name = 3
        self.farm_cooldown_seconds = 60
        self.char_money = '¢'

    @property
    def default_last_farm(self):
        return 0