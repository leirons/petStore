from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db.sessions import Base


class Store(Base):
    __tablename__ = "store"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pet.id"))
    pet = relationship("Pet", back_populates="store")
    quantity = Column(Integer)
    status = Column(String)
    complete = Column(Boolean, default=True)
