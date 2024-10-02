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


# Добавление нового товара
def add_cat(db: Session, cat: shemas.CatCreate) -> models.Cat:
    db_product = models.Cat(**cat.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def add_cat_breed(db: Session, cat_breed: shemas.CatBreedCreate) -> models.CatBreed:
    db_product = models.CatBreed(**cat_breed.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
#
# # Добавление нового типа продукта
# def add_product_type(db: Session,
#                      product_type: shemas.ProductTypeCreate) \
#         -> models.ProductType:
#     db_product_type = models.ProductType(**product_type.dict())
#     db.add(db_product_type)
#     db.commit()
#     db.refresh(db_product_type)
#     return db_product_type
#
#
# # Получение всех товаров по типу
# def get_products_type(db: Session,
#                       type_id: int) -> models.Product:
#     result = db.query(models.Product).\
#         filter(models.Product.product_type_id == type_id).all()
#     return result
