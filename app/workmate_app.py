import uvicorn
from fastapi import FastAPI, HTTPException, Depends
import models
import shemas
from sqlalchemy.orm import Session
import crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/breeds", response_model=list[shemas.CatBreed],
         summary="Получение всех пород",
         description="При запросе выводятся все "
                     "породы, содержащиеся в базе данных")
def read_cat_breeds(db: Session = Depends(get_db)):
    db_breeds = crud.get_breeds(db)
    if db_breeds is None:
        raise HTTPException(status_code=404, detail="Products not found")
    return db_breeds


@app.get("/cats", response_model=list[shemas.CatBase],
         summary="Получение списка всех котят",
         description="При запросе выводится список всех "
                     "котят, содержащихся в базе данных")
def read_cats(db: Session = Depends(get_db)):
    db_products = crud.get_cats(db)
    if db_products is None:
        raise HTTPException(status_code=404, detail="Products not found")
    return db_products


@app.post("/cat", response_model=shemas.Cat,
          summary="Добавление котёнка",
          description="При отправке запросе в "
                      "базу данных добавляется информация о новом котёнке")
def create_cat(cat: shemas.CatCreate,
               db: Session = Depends(get_db)):
    return crud.add_cat(db=db, cat=cat)

@app.get("/cat/{id}",
          summary="Удаление информации о котёнка",
          description="При отправке запросе в "
                      "базу данных удаляется информация о котёнке")
def clear_cat(id: int, db: Session = Depends(get_db)):
    return crud.delete_cat(db=db, cat_id=id)

@app.post("/cat_breed", response_model=shemas.CatBreed,
          summary="Добавление породы котят",
          description="При отправке запросе в "
                      "базу данных добавляется новая порода котят")
def create_cat_breed(cat_breed: shemas.CatBreedCreate,
               db: Session = Depends(get_db)):
    return crud.add_cat_breed(db=db, cat_breed=cat_breed)


@app.get("/cats/{id}", response_model=list[shemas.Cat],
         summary="Получение данных по котёнку",
         description="При отправке запросе выводится характеристики запрашиваемого котёнка")
def read_cat(id: int, db: Session = Depends(get_db)):
    db_product = crud.get_cat_id(db=db, cat_id=id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_product


# @app.get("/products/type/{type_id}", response_model=list[shemas.Product],
#          summary="Получение продуктов по типу",
#          description="При отправке запросе выводятся "
#                      "продукты по запрашиваемому типу")
# def read_products_type(type_id: int, db: Session = Depends(get_db)):
#     db_products_type = crud.get_products_type(db=db, type_id=type_id)
#     if db_products_type is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_products_type


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
