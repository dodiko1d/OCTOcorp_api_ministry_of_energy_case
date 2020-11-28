""" Site paths work control - call necessary controllers. """

from fastapi import APIRouter, Depends, HTTPException
from . import schemas, controller
from sqlalchemy.orm import Session
from database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get('/get-first-time-of-prediction/{city_name}', summary='Первое обновление прогноза по городу.')
async def get_city_data(city_name: str, db: Session = Depends(get_db)):
    data = controller.get_city_data(db, city_name)
    return data


@router.get('/get-last-time-of-prediction/{city_name}', summary='Последнее обновление прогноза по городу.')
async def get_city_data(city_name: str, db: Session = Depends(get_db)):
    data = controller.get_city_data(db, city_name)
    return data


@router.get('/get-city-data/{city_name}', summary='Получить данные по городу на определённое время.')
async def get_city_data(city_name: str, db: Session = Depends(get_db)):
    data = controller.get_city_data(db, city_name)
    return data
