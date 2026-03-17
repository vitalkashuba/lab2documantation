from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data_access.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    reviews = relationship("Review", back_populates="user")