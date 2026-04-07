"""
Container — DI-контейнер (аналог container.ts з TSyringe).
Реєструє залежності вручну через Python-клас замість декораторів.
"""
from sqlalchemy.orm import Session

from src.dal.data_source import initialize, get_session
from src.dal.repositories.repositories import CsvReader, UserRepository, HotelRepository, ReviewRepository
from src.bll.services.data_import_service import DataImportService


class Container:
    """Простий DI-контейнер: зберігає та надає залежності."""

    def __init__(self):
        self._session: Session | None = None

    def initialize(self, database_url: str = "sqlite:///database.sqlite") -> None:
        initialize(database_url)
        self._session = get_session()
        print("Dependency injection container configured")

    # ── DAL ──────────────────────────────────────────────────────────────────
    def csv_reader(self) -> CsvReader:
        return CsvReader()

    def user_repository(self) -> UserRepository:
        return UserRepository(self._session)

    def hotel_repository(self) -> HotelRepository:
        return HotelRepository(self._session)

    def review_repository(self) -> ReviewRepository:
        return ReviewRepository(self._session)

    # ── BLL ──────────────────────────────────────────────────────────────────
    def data_import_service(self) -> DataImportService:
        return DataImportService(
            csv_reader=self.csv_reader(),
            user_repo=self.user_repository(),
            hotel_repo=self.hotel_repository(),
            review_repo=self.review_repository(),
        )

    def commit(self) -> None:
        if self._session:
            self._session.commit()

    def close(self) -> None:
        if self._session:
            self._session.close()


# Глобальний екземпляр (синглтон)
container = Container()
