from sqlalchemy import Column, Integer, String, ForeignKey
from data_access.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, ForeignKey("places.id"), primary_key=True)
    menu = Column(String)
    rating = Column(Integer)