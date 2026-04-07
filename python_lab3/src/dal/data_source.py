"""
DataSource — конфігурація SQLAlchemy 
Підтримує SQLite за замовчуванням; легко перемкнути на PostgreSQL/MySQL.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.domain.entities.models import Base

# За замовчуванням — SQLite (аналог оригінального проекту)
DATABASE_URL = "sqlite:///database.sqlite"

engine = sessionmaker  # placeholder — ініціалізується в configure()

_engine = None
_SessionLocal = None


def initialize(database_url: str = DATABASE_URL) -> None:
    """Ініціалізує з'єднання з БД і створює всі таблиці."""
    global _engine, _SessionLocal
    _engine = create_engine(database_url, echo=False)
    _SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(_engine)
    print(f"Database connection established: {database_url}")


def get_session() -> Session:
    """Повертає нову сесію SQLAlchemy."""
    if _SessionLocal is None:
        raise RuntimeError("DataSource not initialized. Call initialize() first.")
    return _SessionLocal()
