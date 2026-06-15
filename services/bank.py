import logging
import json
import uuid
from database.db_manager import db
from config import Config
from services.user import User

logger = logging.getLogger(__name__)


class BankData:
    # Класс для управления даннами банка
    def __init__(self, path):
        self.bank_path = path

    def data_load(self):
        # Возвращает данные банка
        with open(bank_path, 'r') as f:
            return json.load(f)

    def data_save(self, data):
        # Сохраняет данные банка
        with open(self.bank_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def create_transaction(self, user_sender: User = None, user_recipient: User, amount: int, fee: int):
        """
        Создание транзакции между двумя пользователями.

        Args:
            user_sender (User) - объект отправителя
            user_recipient (User) - объект получателя
            amount (int) - сумма перевода в центах
            fee (int) -  сумма комиссии в центах
        """
        sender_id = user_sender.data.id if user_sender else None
        recipient_id = user_recipient.data.id

        # Создание транзакции в таблице
        uuid_str = uuid.uuid4()
        uuid_bytes = uuid_str.bytes

        db.execute(
            "INSERT INTO transactions (id, sender, recipient, amount_sent, fee) VALUES (?, ?, ?, ?)",
            (uuid_bytes, sender_id, recipient_id, amount, fee)
        )

        logger.info(f"Create transaction: UUID: {uuid_str}, amount: {amount}")

class Bank:
    def __init__(self):
        self.bank_path = Config.bank_path
        self.data = BankData(self.bank_path)

