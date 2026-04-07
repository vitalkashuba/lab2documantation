"""
DataImportService — BLL-сервіс імпорту даних.
Точний аналог TypeScript-класу DataImportService з тією ж логікою:
  1. Читає CSV
  2. Дедуплікує користувачів і готелі
  3. Зберігає в БД через репозиторії (DAL)
  4. Оновлює середні рейтинги
"""
from datetime import datetime

from src.bll.interfaces.i_data_import_service import IDataImportService
from src.dal.interfaces.repositories import ICsvReader, IUserRepository, IHotelRepository, IReviewRepository
from src.domain.entities.models import User, Hotel, Review
from src.domain.enums.review_status import ReviewStatus


class DataImportService(IDataImportService):

    def __init__(
        self,
        csv_reader:       ICsvReader,
        user_repo:        IUserRepository,
        hotel_repo:       IHotelRepository,
        review_repo:      IReviewRepository,
    ):
        self._csv_reader  = csv_reader
        self._user_repo   = user_repo
        self._hotel_repo  = hotel_repo
        self._review_repo = review_repo

    # ── public ────────────────────────────────────────────────────────────────
    def import_from_csv(self, file_path: str) -> None:
        print("Reading CSV file...")
        rows = self._csv_reader.read_csv(file_path)

        if not rows:
            print("No data found in CSV file")
            return

        print(f"Found {len(rows)} rows in CSV file")
        print("Processing CSV data...")

        users_map:  dict[str, User]  = {}   # email → User
        hotels_map: dict[str, Hotel] = {}   # name  → Hotel
        raw_reviews: list[dict]      = []

        for row in rows:
            # ── користувач ──────────────────────────────────────────────────
            email = row["userEmail"]
            if email not in users_map:
                user = User(username=row["username"], email=email)
                users_map[email] = user

            # ── готель ──────────────────────────────────────────────────────
            entity_type = row.get("entityType", "")
            entity_name = row.get("entityName", "")

            if entity_type == "hotel" and entity_name not in hotels_map:
                hotel = Hotel(
                    name=entity_name,
                    address=row.get("entityAddress", ""),
                    average_rating=0.0,
                    stars=int(row.get("stars", 3)),
                )
                hotels_map[entity_name] = hotel

            # ── відгук ──────────────────────────────────────────────────────
            if entity_type == "hotel":
                raw_reviews.append({
                    "user_email":  email,
                    "entity_name": entity_name,
                    "comment":     row.get("comment", ""),
                    "rating":      int(row.get("rating", 3)),
                    "date":        self._parse_date(row.get("date", "")),
                    "status":      self._parse_status(row.get("status", "PENDING")),
                })

        # ── збереження користувачів ──────────────────────────────────────────
        print(f"Saving {len(users_map)} users...")
        saved_users = self._user_repo.save_many(list(users_map.values()))
        email_to_id: dict[str, int] = {u.email: u.id for u in saved_users}

        # ── збереження готелів ───────────────────────────────────────────────
        print(f"Saving {len(hotels_map)} hotels...")
        saved_hotels = self._hotel_repo.save_many(list(hotels_map.values()))
        name_to_id: dict[str, int] = {h.name: h.id for h in saved_hotels}

        # ── збереження відгуків ──────────────────────────────────────────────
        print(f"Creating {len(raw_reviews)} reviews...")
        reviews: list[Review] = []
        for rv in raw_reviews:
            review = Review(
                comment=rv["comment"],
                rating=rv["rating"],
                date=rv["date"],
                status=rv["status"],
                user_id=email_to_id[rv["user_email"]],
                hotel_id=name_to_id[rv["entity_name"]],
            )
            reviews.append(review)

        print(f"Saving {len(reviews)} reviews...")
        self._review_repo.save_many(reviews)

        # ── оновлення середніх рейтингів ─────────────────────────────────────
        print("Updating average ratings...")
        self._update_average_ratings()

        print("Data import completed successfully!")

    # ── private ───────────────────────────────────────────────────────────────
    def _update_average_ratings(self) -> None:
        hotels = self._hotel_repo.find_all()
        for hotel in hotels:
            reviews = self._review_repo.find_by_hotel_id(hotel.id)
            if reviews:
                total = sum(r.rating for r in reviews)
                hotel.average_rating = round(total / len(reviews), 1)
                self._hotel_repo.save(hotel)

    @staticmethod
    def _parse_date(raw: str) -> datetime:
        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(raw.strip(), fmt)
            except ValueError:
                continue
        return datetime.utcnow()

    @staticmethod
    def _parse_status(raw: str) -> ReviewStatus:
        try:
            return ReviewStatus(raw.strip().upper())
        except ValueError:
            return ReviewStatus.PENDING
