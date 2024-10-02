from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CatBreedBase(BaseModel):
    breed: str


class CatBreedCreate(CatBreedBase):
    breed: str


class CatBreed(CatBreedBase):
    id: int
    breed: str
    time_created: datetime

    class Config:
        from_attributes = True


class CatBase(BaseModel):
    name: str


class CatCreate(CatBase):
    name: str
    age: str
    weight: float
    color: str
    cat_breed_id: int


class Datetime:
    pass


class Cat(CatBase):
    id: int
    time_created: datetime
    time_updated: Optional[datetime]
    name: str
    age: str
    weight: float
    color: str
    breed: CatBreed

    class Config:
        from_attributes = True
