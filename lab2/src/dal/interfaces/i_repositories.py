from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.models import User, Hotel, Review


class IUserRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[User]: pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]: pass

    @abstractmethod
    def find_all(self) -> List[User]: pass

    @abstractmethod
    def save(self, user: User) -> User: pass

    @abstractmethod
    def save_many(self, users: List[User]) -> List[User]: pass


class IHotelRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Hotel]: pass

    @abstractmethod
    def find_all(self) -> List[Hotel]: pass

    @abstractmethod
    def save(self, hotel: Hotel) -> Hotel: pass

    @abstractmethod
    def save_many(self, hotels: List[Hotel]) -> List[Hotel]: pass


class IReviewRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Review]: pass

    @abstractmethod
    def find_all(self) -> List[Review]: pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Review]: pass

    @abstractmethod
    def find_by_hotel_id(self, hotel_id: int) -> List[Review]: pass

    @abstractmethod
    def save(self, review: Review) -> Review: pass

    @abstractmethod
    def save_many(self, reviews: List[Review]) -> List[Review]: pass
