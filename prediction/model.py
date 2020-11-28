""" Database Product Model. """

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Prediction(Base):
    __tablename__ = 'prediction'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    timestamp = Column(DateTime)
    prediction = Column(Float)
    city = relationship('City', back_populates='predictions')

