"""
DAL Repositories — конкретні реалізації інтерфейсів DAL.
Аналог TypeScript-класів: CsvReader, UserRepository, HotelRepository, ReviewRepository
"""
import csv
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.dal.interfaces.repositories import ICsvReader, IUserRepository, IHotelRepository, IReviewRepository
from src.domain.entities.models import User, Hotel, Review
from src.domain.enums.review_status import ReviewStatus


# ── CsvReader ─────────────────────────────────────────────────────────────────
class CsvReader(ICsvReader):
    """Зчитує CSV-файл через вбудований модуль csv (аналог csv-parser у Node.js)."""

    def read_csv(self, file_path: str) -> list[dict]:
        rows: list[dict] = []
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        return rows


# ── UserRepository ────────────────────────────────────────────────────────────
class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, username: str, email: str) -> User:
        user = User(username=username, email=email)
        self._session.add(user)
        self._session.flush()
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._session.get(User, user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        return self._session.query(User).filter_by(email=email).first()

    def find_all(self) -> list[User]:
        return self._session.query(User).all()

    def save(self, user: User) -> User:
        self._session.add(user)
        self._session.flush()
        return user

    def save_many(self, users: list[User]) -> list[User]:
        self._session.add_all(users)
        self._session.flush()
        return users


# ── HotelRepository ───────────────────────────────────────────────────────────
class HotelRepository(IHotelRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, name: str, address: str, stars: int, average_rating: float = 0.0) -> Hotel:
        hotel = Hotel(name=name, address=address, stars=stars, average_rating=average_rating)
        self._session.add(hotel)
        self._session.flush()
        return hotel

    def find_by_id(self, hotel_id: int) -> Optional[Hotel]:
        return self._session.get(Hotel, hotel_id)

    def find_all(self) -> list[Hotel]:
        return self._session.query(Hotel).all()

    def save(self, hotel: Hotel) -> Hotel:
        self._session.add(hotel)
        self._session.flush()
        return hotel

    def save_many(self, hotels: list[Hotel]) -> list[Hotel]:
        self._session.add_all(hotels)
        self._session.flush()
        return hotels


# ── ReviewRepository ──────────────────────────────────────────────────────────
class ReviewRepository(IReviewRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, comment: str, rating: int, date, status, user_id: int, hotel_id: int) -> Review:
        review = Review(
            comment=comment, rating=rating, date=date,
            status=status, user_id=user_id, hotel_id=hotel_id,
        )
        self._session.add(review)
        self._session.flush()
        return review

    def find_by_id(self, review_id: int) -> Optional[Review]:
        return self._session.get(Review, review_id)

    def find_all(self) -> list[Review]:
        return self._session.query(Review).all()

    def find_by_user_id(self, user_id: int) -> list[Review]:
        return self._session.query(Review).filter_by(user_id=user_id).all()

    def find_by_hotel_id(self, hotel_id: int) -> list[Review]:
        return self._session.query(Review).filter_by(hotel_id=hotel_id).all()

    def save(self, review: Review) -> Review:
        self._session.add(review)
        self._session.flush()
        return review

    def save_many(self, reviews: list[Review]) -> list[Review]:
        self._session.add_all(reviews)
        self._session.flush()
        return reviews
