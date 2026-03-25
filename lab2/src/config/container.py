from src.dal.data_source import init_db, get_session
from src.dal.repositories.csv_reader import CsvReader
from src.dal.repositories.repositories import UserRepository, HotelRepository, ReviewRepository
from src.bll.services.data_import_service import DataImportService
from src.bll.interfaces.i_data_import_service import IDataImportService


class Container:
    """
    DI-контейнер — аналог tsyringe.
    BLL отримує інтерфейси DAL через конструктор (Dependency Injection).
    """

    def __init__(self):
        self._service: IDataImportService | None = None

    def configure(self) -> None:
        # Ініціалізація ORM і бази даних
        init_db()
        session = get_session()

        # DAL — реєстрація імплементацій
        csv_reader   = CsvReader()
        user_repo    = UserRepository(session)
        hotel_repo   = HotelRepository(session)
        review_repo  = ReviewRepository(session)

        # BLL — отримує інтерфейси (не класи) DAL
        self._service = DataImportService(
            csv_reader        = csv_reader,
            user_repository   = user_repo,
            hotel_repository  = hotel_repo,
            review_repository = review_repo,
        )

        print("Dependency injection container configured")

    def resolve(self) -> IDataImportService:
        if self._service is None:
            raise RuntimeError("Container not configured. Call container.configure() first.")
        return self._service


container = Container()
