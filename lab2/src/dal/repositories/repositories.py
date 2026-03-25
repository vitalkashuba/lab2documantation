from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.entities.models import User, Hotel, Review
from src.dal.interfaces.i_repositories import IUserRepository, IHotelRepository, IReviewRepository


# ─────────────────────────────────────────────────────────────────────────────
class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, id: int) -> Optional[User]:
        return self._session.get(User, id)

    def find_by_email(self, email: str) -> Optional[User]:
        return self._session.query(User).filter_by(email=email).first()

    def find_all(self) -> List[User]:
        return self._session.query(User).all()

    def save(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def save_many(self, users: List[User]) -> List[User]:
        self._session.add_all(users)
        self._session.commit()
        for u in users:
            self._session.refresh(u)
        return users


# ─────────────────────────────────────────────────────────────────────────────
class HotelRepository(IHotelRepository):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, id: int) -> Optional[Hotel]:
        return self._session.get(Hotel, id)

    def find_all(self) -> List[Hotel]:
        return self._session.query(Hotel).all()

    def save(self, hotel: Hotel) -> Hotel:
        self._session.add(hotel)
        self._session.commit()
        self._session.refresh(hotel)
        return hotel

    def save_many(self, hotels: List[Hotel]) -> List[Hotel]:
        self._session.add_all(hotels)
        self._session.commit()
        for h in hotels:
            self._session.refresh(h)
        return hotels


# ─────────────────────────────────────────────────────────────────────────────
class ReviewRepository(IReviewRepository):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, id: int) -> Optional[Review]:
        return self._session.get(Review, id)

    def find_all(self) -> List[Review]:
        return self._session.query(Review).all()

    def find_by_user_id(self, user_id: int) -> List[Review]:
        return self._session.query(Review).filter_by(user_id=user_id).all()

    def find_by_hotel_id(self, hotel_id: int) -> List[Review]:
        return self._session.query(Review).filter_by(hotel_id=hotel_id).all()

    def save(self, review: Review) -> Review:
        self._session.add(review)
        self._session.commit()
        self._session.refresh(review)
        return review

    def save_many(self, reviews: List[Review]) -> List[Review]:
        self._session.add_all(reviews)
        self._session.commit()
        for r in reviews:
            self._session.refresh(r)
        return reviews
