from datetime import datetime
from src.bll.interfaces.i_data_import_service import IDataImportService
from src.dal.interfaces.i_csv_reader import ICsvReader
from src.dal.interfaces.i_repositories import IUserRepository, IHotelRepository, IReviewRepository
from src.domain.entities.models import User, Hotel, Review
from src.domain.enums.review_status import ReviewStatus


class DataImportService(IDataImportService):
    """
    Рівень бізнес-логіки.
    Використовує ІНТЕРФЕЙСИ DAL (не імплементацію) — IoC / DI.
    """

    def __init__(
        self,
        csv_reader:        ICsvReader,
        user_repository:   IUserRepository,
        hotel_repository:  IHotelRepository,
        review_repository: IReviewRepository,
    ):
        self._csv_reader        = csv_reader
        self._user_repository   = user_repository
        self._hotel_repository  = hotel_repository
        self._review_repository = review_repository

    # ─────────────────────────────────────────────────────────────────────────
    def import_from_csv(self, file_path: str) -> None:
        print("Reading CSV file...")
        rows = self._csv_reader.read_csv(file_path)

        if not rows:
            print("No data found in CSV file")
            return

        print(f"Found {len(rows)} rows in CSV file")
        print("Processing CSV data...")

        users_map:  dict[str, User]  = {}
        hotels_map: dict[str, Hotel] = {}
        pending_reviews = []

        for row in rows:
            # ── Унікальні користувачі ────────────────────────────────────────
            email = row["userEmail"]
            if email not in users_map:
                user          = User()
                user.username = row["username"]
                user.email    = email
                users_map[email] = user

            # ── Унікальні готелі ─────────────────────────────────────────────
            if row["entityType"] == "hotel":
                hotel_name = row["entityName"]
                if hotel_name not in hotels_map:
                    hotel                = Hotel()
                    hotel.name           = hotel_name
                    hotel.address        = row["entityAddress"]
                    hotel.average_rating = 0.0
                    hotel.stars          = int(row["stars"])
                    hotels_map[hotel_name] = hotel

                pending_reviews.append({
                    "user_email": email,
                    "hotel_name": hotel_name,
                    "comment":    row["comment"],
                    "rating":     int(row["rating"]),
                    "date":       datetime.strptime(row["date"], "%Y-%m-%d"),
                    "status":     ReviewStatus(row["status"]),
                })

        # ── Зберегти користувачів ────────────────────────────────────────────
        print(f"Saving {len(users_map)} users...")
        saved_users  = self._user_repository.save_many(list(users_map.values()))
        email_to_id  = {u.email: u.id for u in saved_users}

        # ── Зберегти готелі ──────────────────────────────────────────────────
        print(f"Saving {len(hotels_map)} hotels...")
        saved_hotels = self._hotel_repository.save_many(list(hotels_map.values()))
        name_to_id   = {h.name: h.id for h in saved_hotels}

        # ── Створити та зберегти відгуки ─────────────────────────────────────
        print(f"Creating {len(pending_reviews)} reviews...")
        review_entities: list[Review] = []
        for data in pending_reviews:
            review          = Review()
            review.comment  = data["comment"]
            review.rating   = data["rating"]
            review.date     = data["date"]
            review.status   = data["status"]
            review.user_id  = email_to_id[data["user_email"]]
            review.hotel_id = name_to_id[data["hotel_name"]]
            review_entities.append(review)

        print(f"Saving {len(review_entities)} reviews...")
        self._review_repository.save_many(review_entities)

        # ── Оновити середні рейтинги ─────────────────────────────────────────
        print("Updating average ratings...")
        self._update_average_ratings()

        print("Data import completed successfully!")

    # ─────────────────────────────────────────────────────────────────────────
    def _update_average_ratings(self) -> None:
        for hotel in self._hotel_repository.find_all():
            reviews = self._review_repository.find_by_hotel_id(hotel.id)
            if reviews:
                hotel.average_rating = sum(r.rating for r in reviews) / len(reviews)
                self._hotel_repository.save(hotel)
