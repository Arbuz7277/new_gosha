import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.token = os.getenv('API_KEY')

        if not self.token:
            raise ValueError("API_KEY not found in .env file!")