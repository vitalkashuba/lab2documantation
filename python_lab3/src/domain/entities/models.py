from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship, DeclarativeBase
from src.domain.enums.review_status import ReviewStatus


class Base(DeclarativeBase):
    pass


# ── ReviewableEntity (аналог абстрактного базового класу з TypeORM) ──────────
class ReviewableEntity(Base):
    """Абстрактний базовий клас для сутностей, що мають відгуки."""
    __tablename__ = "reviewable_entity"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String, nullable=False)
    address       = Column(String, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)
    type          = Column(String(50))          # discriminator колонка

    __mapper_args__ = {
        "polymorphic_on":      type,
        "polymorphic_identity": "reviewable_entity",
    }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"


# ── Hotel (наслідує ReviewableEntity) ────────────────────────────────────────
class Hotel(ReviewableEntity):
    """Готель — успадковує ReviewableEntity, додає stars та зв'язок з відгуками."""
    __tablename__ = "hotel"

    id    = Column(Integer, ForeignKey("reviewable_entity.id"), primary_key=True)
    stars = Column(Integer, nullable=False)

    reviews = relationship("Review", back_populates="hotel", cascade="all, delete-orphan")

    __mapper_args__ = {"polymorphic_identity": "hotel"}

    def __repr__(self) -> str:
        return f"<Hotel id={self.id} name={self.name!r} stars={self.stars}>"


# ── User ──────────────────────────────────────────────────────────────────────
class User(Base):
    """Користувач платформи."""
    __tablename__ = "user"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email    = Column(String, nullable=False, unique=True)

    reviews  = relationship("Review", back_populates="user")

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} email={self.email!r}>"


# ── Review ────────────────────────────────────────────────────────────────────
class Review(Base):
    """Відгук користувача про готель."""
    __tablename__ = "review"

    id      = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(String, nullable=False)
    rating  = Column(Integer, nullable=False)
    date    = Column(DateTime, default=datetime.utcnow, nullable=False)
    status  = Column(SAEnum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False)

    user_id  = Column(Integer, ForeignKey("user.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)

    user  = relationship("User",  back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review id={self.id} rating={self.rating} status={self.status}>"
