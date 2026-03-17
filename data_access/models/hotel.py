from sqlalchemy import Column, Integer, ForeignKey
from data_access.database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, ForeignKey("places.id"), primary_key=True)
    user_rating = Column(Integer)
    stars = Column(Integer)