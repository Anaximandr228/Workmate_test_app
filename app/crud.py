from sqlalchemy.orm import Session
from app import models
from app import shemas


# Получение всех котят
def get_cats(db: Session) -> list[models.Cat]:
    result = db.query(models.Cat).all()
    return result


# Получение всех пород
def get_breeds(db: Session) -> list[models.CatBreed]:
    result = db.query(models.CatBreed).all()
    return result


# Получение всх котят по породе
def get_cats_breeds(db: Session, breed_id: int) -> list[models.Cat]:
    result = db.query(models.Cat).filter(models.Cat.cat_breed_id == breed_id).all()
    return result


# Удаление информации о котёнке
def delete_cat(db: Session, cat_id: int):
    db_product = \
        db.query(models.Cat).filter(models.Cat.id == cat_id).one()
    db.delete(db_product)
    db.commit()
    return {"message": "Данные были удалены"}


# Получение информации о определенном котёнке
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


# Обновление данных о котёнке
def update_cat(db: Session, cat_id: int, cat: shemas.CatCreate) -> models.Cat:
    db_product = db.query(models.Cat).filter_by(id=cat_id)
    db_product.update(cat.dict(), synchronize_session='fetch')
    db.commit()
    db_product = db.query(models.Cat).filter(models.Cat.id == cat_id).all()
    return db_product


# Добавление новой породы
def add_cat_breed(db: Session, cat_breed: shemas.CatBreedCreate) -> models.CatBreed:
    db_product = models.CatBreed(**cat_breed.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
