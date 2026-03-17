from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from data_access.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    text = Column(String)
    rating = Column(Integer)
    date = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("places.id"))

    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")