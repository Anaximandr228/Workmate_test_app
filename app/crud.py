from sqlalchemy.orm import Session
from app import models
from app import shemas


# Получение всех товаров
def get_cats(db: Session) -> list[models.Cat]:
    result = db.query(models.Cat).all()
    return result


def get_breeds(db: Session) -> list[models.CatBreed]:
    result = db.query(models.CatBreed).all()
    return result


def get_cats_breeds(db: Session, breed_id: int) -> list[models.Cat]:
    result = db.query(models.Cat).filter(models.Cat.cat_breed_id == breed_id).all()
    return result

# Получение товара по id
def delete_cat(db: Session, cat_id: int):
    db_product = \
        db.query(models.Cat).filter(models.Cat.id == cat_id).one()
    db.delete(db_product)
    db.commit()
    return {"message": "Данные были удалены"}


def get_cat_id(db: Session, cat_id: int) -> models.Cat:
    db_product = \
        db.query(models.Cat).filter(models.Cat.id == cat_id).all()
    return db_product


# Добавление данных о котёнке
def add_cat(db: Session, cat: shemas.CatCreate) -> models.Cat:
    db_product = models.Cat(**cat.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_cat(db: Session,cat_id: int, cat: shemas.CatCreate) -> models.Cat:
    db_product = db.query(models.Cat).filter_by(id=cat_id)
    db_product.update(cat.dict(), synchronize_session='fetch')
    db.commit()
    db_product = db.query(models.Cat).filter(models.Cat.id == cat_id).all()
    return db_product


def add_cat_breed(db: Session, cat_breed: shemas.CatBreedCreate) -> models.CatBreed:
    db_product = models.CatBreed(**cat_breed.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

