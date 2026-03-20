import os
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
        self.json_users_path = self.dp_path / 'users.json'

    @property
    def default_last_farm(self):
        return 0