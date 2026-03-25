from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.domain.entities.models import Base

DATABASE_URL = "sqlite:///database.sqlite"

_engine = create_engine(DATABASE_URL, echo=False)
_SessionLocal = sessionmaker(bind=_engine)


def init_db() -> None:
    """Створює всі таблиці (аналог synchronize:true у TypeORM)."""
    Base.metadata.create_all(bind=_engine)
    print("Database connection established")


def get_session() -> Session:
    return _SessionLocal()
