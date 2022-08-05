from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from core.db.sessions import Base


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    pet_id = Column(Integer, ForeignKey("pet.id",ondelete="CASCADE"))
    pet_tag = relationship("Pet", back_populates='tag', cascade="all,delete")


class Pet(Base):
    __tablename__ = "pet"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    status = Column(String)
    category = Column(JSON)
    store = relationship("Store", back_populates="pet_store")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="pet")

    tag = relationship("Tag", back_populates="pet_tag", cascade="all,delete")
