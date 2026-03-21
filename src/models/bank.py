import time
import secrets
import logging
from datetime import datetime, timezone

from src.models.database import Database
from src.models.user import User
from src.config import Config

logger = logging.getLogger(__name__)
cfg = Config()
dp = Database()

class Bank:
    def __init__(self):
        self.data = dp.load_bank()
        self.max_id = self.data['max_check_id']

    def create_check(self,
                     amount: float,
                     commision_precent: float,
                     sender: int,
                     recipient: int,
                     type: str = cfg.TRANSFER,
                     description: str = "Not"):
        self.data['max_check_id'] += 1

        check = self.data.setdefault(str(self.data['max_check_id']), {})
        check['id'] = self.data['max_check_id']
        check['key'] = "CH:" + ''.join([secrets.choice(cfg.chars_check_key) for _ in range(cfg.len_check_key)])
        check['created_at'] = f"{datetime.now(timezone.utc)}"
        check['amount'] = amount
        check['commission_precent'] = commision_precent
        check['commission_money'] = amount * commision_precent
        check['received'] = amount - (check['commission_money'])
        check['sender'] = sender
        check['recipient'] = recipient
        check['type'] = type
        check['description'] = description

        self.add_money(recipient, check['received'])
        self.remove_money(sender, amount)

        dp.save_bank(self.data)

        logger.info(f"Created check #{check['id']} of type {check['type']}")

    def add_money(self, uid, money):
        if money < 0:
            raise ValueError("argument 'money' cannot be negative.")

        user = dp.load_user(uid)
        user['balance'] += money
        dp.save_user(user)

        logger.debug(f"Added {money} cent to {uid}")

    def remove_money(self, uid, money):
        if money < 0:
            raise ValueError("argument 'money' cannot be negative.")

        user = dp.load_user(uid)
        user['balance'] -= money
        dp.save_user(user)

        logger.debug(f"Removed {money} cent to {uid}")