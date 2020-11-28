""" Database Prediction Model. """

from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    first_prediction_datetime = Column(DateTime, nullable=True)
    last_prediction_datetime = Column(DateTime, nullable=True)
    predictions = relationship('Prediction', back_populates='city')

