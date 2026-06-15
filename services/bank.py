import logging
import json
import uuid
from database.db_manager import db
from config import Config
from services.user import User
import os

logger = logging.getLogger(__name__)


class BankData:
    # Класс для управления даннами банка
    def __init__(self, path):
        self.bank_path = path

        # Создаем файл при его отсутствии
        if not os.path.exists(self.bank_path):
            data = {"balance": 0}
            with open(self.bank_path, 'w') as f:
                json.dump(data, f, indent=4)

    def data_load(self):
        # Возвращает данные банка
        with open(self.bank_path, 'r') as f:
            return json.load(f)

    def data_save(self, data):
        # Сохраняет данные банка
        with open(self.bank_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    async def create_transaction(self, recipient_id: int, amount: int, fee: int | None = None, sender_id: int | None = None) -> None:
        """
        Создание транзакции между двумя пользователями.

        Args:
            sender_id (int) - айди отправителя
            recipient_id (int) - айди получателя
            amount (int) - сумма перевода в центах
            fee (int) -  сумма комиссии в центах
        """
        # Значение по умолчанию
        fee = fee if fee else 0

        data = self.data_load()

        # Берем центы из банка, если нет отправителя
        if not sender_id:
            if data['balance'] < amount:
                raise ValueError("Insufficient funds in the bank.")
            data['balance'] -= amount

        # Создание транзакции в таблице
        uuid_str = uuid.uuid4()
        uuid_bytes = uuid_str.bytes
        await db.execute(
            "INSERT INTO transactions (id, sender, recipient, amount_sent, fee) VALUES (?, ?, ?, ?)",
            (uuid_bytes, sender_id, recipient_id, amount, fee)
        )

        # Добавление комиссии в банк
        data['balance'] += fee

        logger.info(f"Create transaction: UUID: {uuid_str}, amount: {amount}")

class Bank:
    def __init__(self):
        self.bank_path = Config.bank_path
        self.data = BankData(self.bank_path)

    async def transaction(self, user_sender: User, user_recipient: User, amount: int, fee_percent: float) -> None:
        """
        :param user_sender: объект отправителя
        :param user_recipient: объект получателя
        :param amount: сумма перевода в центах
        :param fee_percent: комиссия в процентах
        """

        # Минимальная сумма
        if amount < Config.transaction.min_amount:
            raise ValueError("The amount is less than the minimum value.")

        # Перевод самому себе
        if user_sender == user_recipient:
            raise ValueError("A transaction to oneself is not possible.")

        # Комиссия минимум 1 цент
        fee = max(1, int(amount * fee_percent))

        # Транзакция
        await self.data.create_transaction(user_recipient.data.id, amount, fee, user_sender.data.id)

    async def add_money(self, user_recipient: User, amount: int) -> None:
        """
        :param user_recipient: объект получателя
        :param amount: сумма в центах
        """
        data = self.data.data_load()
        await self.data.create_transaction(user_recipient.data.id, amount)

bank = Bank()