from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship, DeclarativeBase
from src.domain.enums.review_status import ReviewStatus


class Base(DeclarativeBase):
    pass


# ─────────────────────────────────────────────────────────────────────────────
# ReviewableEntity  –  Single Table Inheritance (аналог @TableInheritance у TypeORM)
# ─────────────────────────────────────────────────────────────────────────────
class ReviewableEntity(Base):
    __tablename__ = "reviewable_entity"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    name           = Column(String,  nullable=False)
    address        = Column(String,  nullable=False)
    average_rating = Column(Float,   default=0.0)
    entity_type    = Column(String(50), nullable=False)   # discriminator

    __mapper_args__ = {
        "polymorphic_on":       "entity_type",
        "polymorphic_identity": "reviewable_entity",
    }


# ─────────────────────────────────────────────────────────────────────────────
# Hotel  –  @ChildEntity у TypeORM
# ─────────────────────────────────────────────────────────────────────────────
class Hotel(ReviewableEntity):
    stars   = Column(Integer)
    reviews = relationship("Review", back_populates="hotel")

    __mapper_args__ = {"polymorphic_identity": "hotel"}


# ─────────────────────────────────────────────────────────────────────────────
# User
# ─────────────────────────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "user"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String,  nullable=False)
    email    = Column(String,  nullable=False, unique=True)

    reviews  = relationship("Review", back_populates="user")


# ─────────────────────────────────────────────────────────────────────────────
# Review
# ─────────────────────────────────────────────────────────────────────────────
class Review(Base):
    __tablename__ = "review"

    id       = Column(Integer,  primary_key=True, autoincrement=True)
    comment  = Column(String,   nullable=False)
    rating   = Column(Integer,  nullable=False)
    date     = Column(DateTime, nullable=False)
    status   = Column(SAEnum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False)

    user_id  = Column(Integer, ForeignKey("user.id"),                nullable=False)
    hotel_id = Column(Integer, ForeignKey("reviewable_entity.id"),   nullable=False)

    user     = relationship("User",  back_populates="reviews")
    hotel    = relationship("Hotel", back_populates="reviews", foreign_keys=[hotel_id])
