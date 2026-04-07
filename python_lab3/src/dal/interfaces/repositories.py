"""
DAL Interfaces — абстрактні базові класи

"""
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.models import User, Hotel, Review


# ── ICsvReader ────────────────────────────────────────────────────────────────
class ICsvReader(ABC):
    @abstractmethod
    def read_csv(self, file_path: str) -> list[dict]:
        """Зчитати CSV-файл і повернути список рядків як словників."""
        ...


# ── IUserRepository ───────────────────────────────────────────────────────────
class IUserRepository(ABC):
    @abstractmethod
    def create(self, username: str, email: str) -> User: ...

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    def find_all(self) -> list[User]: ...

    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def save_many(self, users: list[User]) -> list[User]: ...


# ── IHotelRepository ──────────────────────────────────────────────────────────
class IHotelRepository(ABC):
    @abstractmethod
    def create(self, name: str, address: str, stars: int, average_rating: float = 0.0) -> Hotel: ...

    @abstractmethod
    def find_by_id(self, hotel_id: int) -> Optional[Hotel]: ...

    @abstractmethod
    def find_all(self) -> list[Hotel]: ...

    @abstractmethod
    def save(self, hotel: Hotel) -> Hotel: ...

    @abstractmethod
    def save_many(self, hotels: list[Hotel]) -> list[Hotel]: ...


# ── IReviewRepository ─────────────────────────────────────────────────────────
class IReviewRepository(ABC):
    @abstractmethod
    def create(self, comment: str, rating: int, date, status, user_id: int, hotel_id: int) -> Review: ...

    @abstractmethod
    def find_by_id(self, review_id: int) -> Optional[Review]: ...

    @abstractmethod
    def find_all(self) -> list[Review]: ...

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> list[Review]: ...

    @abstractmethod
    def find_by_hotel_id(self, hotel_id: int) -> list[Review]: ...

    @abstractmethod
    def save(self, review: Review) -> Review: ...

    @abstractmethod
    def save_many(self, reviews: list[Review]) -> list[Review]: ...
