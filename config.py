from dataclasses import dataclass
from pathlib import Path

@dataclass
class Transaction:
    min_amount: int = 10_00

@dataclass
class Farm:
    min_value: int = 10
    max_value: int = 5_00
    cooldown: int = 60 * 60 * 2  # 2 часа

@dataclass
class Config:
    data_dir: Path = Path("data/")
    database_dir: Path = Path("database/")
    services_dir: Path = Path("services/")
    handlers_dir: Path = Path("handlers/")

    bank_path: Path = data_dir / Path("bank.json")
    db_path: Path = data_dir / Path("bot.db")

    # Остальные конфигурации
    transaction: Transaction = Transaction
    farm: Farm = Farm