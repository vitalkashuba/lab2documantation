from data_access.database import engine, Base, SessionLocal

from data_access.repositories.user_repository import UserRepository
from data_access.repositories.place_repository import PlaceRepository
from data_access.repositories.review_repository import ReviewRepository

from bisness_logic.trip_service import TripService


def main():

    # створення таблиць
    Base.metadata.create_all(engine)

    session = SessionLocal()

    # репозиторії
    user_repo = UserRepository(session)
    place_repo = PlaceRepository(session)
    review_repo = ReviewRepository(session)

    # dependency injection
    service = TripService(
        user_repo,
        place_repo,
        review_repo
    )

    # завантаження CSV
    service.load_csv("tripadvisor_data.csv")

    print("Data imported successfully")


if __name__ == "__main__":
    main()