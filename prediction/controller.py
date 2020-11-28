""" Controllers are containing main part of site's business-logic. """

from sqlalchemy.orm import Session
from sqlalchemy import literal

from . import model, schemas


def new_prediction(db: Session, city, timestamp, prediction):
    db_product = model.Prediction(
        city=city,
        timestamp=timestamp,
        prediction=prediction,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {'status_code': '200'}


def get_city_data(db: Session, city_data: str):
    return len(db.query(model.Prediction)\
               .filter(model.Prediction.city == city_data).all())

