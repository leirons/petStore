from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.db.sessions import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    login = Column(String, index=True, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)

    pet = relationship("Pet", back_populates="user", cascade="all,delete")
