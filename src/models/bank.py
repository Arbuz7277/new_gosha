import time
from datetime import datetime, timezone

from .database import Database
from .. import config

cfg = config.Config()

class Bank:
    def __init__(self):
        dp = Database()
