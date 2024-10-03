import json
from typing import Generator
import psycopg2
import pytest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from app import models
from app.config import user, password, host
from app.workmate_app import app, get_db

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}/test'


@pytest.fixture(scope="session")
def connection():
    con = psycopg2.connect(dbname='postgres',
                           user=user, host=host,
                           password=password)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('DROP DATABASE IF EXISTS test')
    cur.execute("CREATE DATABASE test")

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
    )
    models.Base.metadata.create_all(bind=engine)
    return engine.connect()


@pytest.fixture(scope="session")
def db_session(connection):
    transaction = connection.begin()
    session_factory = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=connection)
    session = session_factory()
    yield session
    transaction.rollback()


@pytest.fixture(scope='module')
def client(db_session) -> Generator:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def cats_setup(db_session):
    db_cat = models.CatBreed(breed='Бирманская кошка')
    db_session.add(db_cat)
    db_session.commit()
    db_breed = models.Cat(name='Барсик', age='3 месяца', weight=0.45, color='Белый', cat_breed_id=1)
    db_session.add(db_breed)
    db_session.commit()


def test_get_cats_list(client, cats_setup):
    print('test_get_cats_list')
    response = client.get("/cats")
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'Барсик'


def test_get_breeds_list(client, cats_setup):
    print('test_get_breeds_list')
    response = client.get("/breeds")
    assert response.status_code == 200
    assert response.json()[0]['breed'] == 'Бирманская кошка'


def test_get_breeds_cats(client, cats_setup):
    print('test_get_breeds_cats')
    response = client.get("/cats/breeds/1")
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'Барсик'


def test_get_cat_id(client, cats_setup):
    print('test_get_cat_id')
    response = client.get("/cats/1")
    assert response.status_code == 200
    assert response.json()[0]['age'] == '3 месяца'


def test_post_cat_breed(client, cats_setup, db_session):
    print('test_post_cat')
    data = {
        "breed": "Сфинкс"
    }
    response = client.post("/breed", data=json.dumps(data))
    saved_product = db_session.query(models.CatBreed). \
        filter(models.CatBreed.id == response.json()["id"]).all()
    assert response.status_code == 200
    assert response.json()['breed'] == 'Сфинкс'
    assert saved_product[0].breed == 'Сфинкс'


def test_post_cat(client, cats_setup, db_session):
    print('test_post_products')
    data = {
        "name": "Пушок",
        "age": "6 месяцев",
        "weight": 0.872,
        "color": "Рыжий",
        "cat_breed_id": 1
    }
    response = client.post("/cat", data=json.dumps(data))
    saved_product = db_session.query(models.Cat). \
        filter(models.Cat.id == response.json()["id"]).all()
    assert response.status_code == 200
    assert response.json()['name'] == 'Пушок'
    assert saved_product[0].name == 'Пушок'


def test_post_update_cat(client, cats_setup, db_session):
    print('test_post_products')
    data = {
        "name": "Пушок",
        "age": "8 месяцев",
        "weight": 1.242,
        "color": "Рыжий",
        "cat_breed_id": 1
    }
    response = client.post("/cat", data=json.dumps(data))
    saved_product = db_session.query(models.Cat). \
        filter(models.Cat.id == response.json()["id"]).all()
    assert response.status_code == 200
    assert response.json()['weight'] == 1.242
    assert saved_product[0].weight == 1.242


def test_get_delete_cat(client, cats_setup):
    print('test_get_delete_cat')
    response = client.get("/cat/1")
    assert response.status_code == 200
    assert response.json()['message'] == 'Данные были удалены'
