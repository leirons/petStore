from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from core.db.sessions import Base


class Pet(Base):
    __tablename__ = "pet"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    status = Column(String)
    category = Column(JSON)
    tags = Column(JSON)
    store = relationship("Store", back_populates="pet")

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="pet")
