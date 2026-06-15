from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    data_dir: Path = Path("data/")
    database_dir: Path = Path("database/")
    services_dir: Path = Path("services/")
    handlers_dir: Path = Path("handlers/")

    bank_path: Path = data_dir / Path("bank.json")
    db_path: Path = data_dir / Path("bot.db")

