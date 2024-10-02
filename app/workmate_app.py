import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from app import models
from app import shemas
from sqlalchemy.orm import Session
from app import crud
from app.database import engine, SessionLocal

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
async def read_cat_breeds(db: Session = Depends(get_db)):
    db_breeds = await crud.get_breeds(db)
    if db_breeds is None:
        raise HTTPException(status_code=404, detail="Products not found")
    return db_breeds


@app.get("/cats", response_model=list[shemas.CatBase],
         summary="Получение списка всех котят",
         description="При запросе выводится список всех "
                     "котят, содержащихся в базе данных")
async def read_cats(db: Session = Depends(get_db)):
    db_cats = await crud.get_cats(db)
    if db_cats is None:
        raise HTTPException(status_code=404, detail="Products not found")
    return db_cats


@app.get("/cats/breeds/{breed_id}", response_model=list[shemas.CatBase],
         summary="Получение списка всех котят по породе",
         description="При запросе выводится список всех "
                     "котят, содержащихся в базе данных")
async def read_cats(breed_id: int, db: Session = Depends(get_db)):
    db_cats = await crud.get_cats_breeds(db=db, breed_id=breed_id)
    if db_cats is None:
        raise HTTPException(status_code=404, detail="Products not found")
    return db_cats


@app.post("/cat", response_model=shemas.Cat,
          summary="Добавление котёнка",
          description="При отправке запросе в "
                      "базу данных добавляется информация о новом котёнке")
async def create_cat(cat: shemas.CatCreate,
               db: Session = Depends(get_db)):
    db_cat =  await crud.add_cat(db=db, cat=cat)
    return db_cat


@app.get("/cat/{id}",
         summary="Удаление информации о котёнка",
         description="При отправке запросе в "
                     "базу данных удаляется информация о котёнке")
async def clear_cat(id: int, db: Session = Depends(get_db)):
    db_cat = await crud.delete_cat(db=db, cat_id=id)
    return db_cat


@app.post("/cat/update/{id}", response_model=list[shemas.Cat],
          summary="Изменение информации о котёнка",
          description="При отправке запросе в "
                      "базу данных изменяется информация о котёнке")
async def change_cat(id: int, cat: shemas.CatCreate, db: Session = Depends(get_db)):
    db_cat = await crud.update_cat(db=db, cat_id=id, cat=cat)
    return db_cat


@app.post("/breed", response_model=shemas.CatBreed,
          summary="Добавление породы котят",
          description="При отправке запросе в "
                      "базу данных добавляется новая порода котят")
async def create_cat_breed(cat_breed: shemas.CatBreedCreate,
                     db: Session = Depends(get_db)):
    db_cat = await crud.add_cat_breed(db=db, cat_breed=cat_breed)
    return db_cat


@app.get("/cats/{id}", response_model=list[shemas.Cat],
         summary="Получение данных по котёнку",
         description="При отправке запросе выводится характеристики запрашиваемого котёнка")
async def read_cat(id: int, db: Session = Depends(get_db)):
    db_cats = await crud.get_cat_id(db=db, cat_id=id)
    if db_cats is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_cats


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
