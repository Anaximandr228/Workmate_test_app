from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


# Определение полей таблицы cat_breed
class CatBreed(Base):
    __tablename__ = "cat_breed"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    breed = Column(String(100), nullable=False)

    cat = relationship("Cat", back_populates="breed")


# Определение полей таблицы cat
class Cat(Base):
    __tablename__ = "cat"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(100), nullable=False)
    age = Column(String(100), nullable=False)
    weight = Column(Float, nullable=False)
    color = Column(String(100), nullable=False)
    cat_breed_id = Column(Integer, ForeignKey("cat_breed.id"))

    breed = relationship("CatBreed", back_populates="cat")
