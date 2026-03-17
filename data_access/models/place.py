from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data_access.database import Base

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    category = Column(String)

    reviews = relationship("Review", back_populates="place")