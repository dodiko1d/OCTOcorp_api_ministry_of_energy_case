import datetime
from prediction import Prediction
import random
from sqlalchemy.orm import Session


class FakePredictionsGenerator:
    """ Fake predictions generator for tests. """

    def __init__(self, database: Session) -> None:
        self.__database = database
        self.__fake_predictions_generation()

    def __fake_predictions_generation(self) -> None:
        for hour in range(24 * 360):
            db_product = Prediction(
                city_id=0,
                timestamp=datetime.datetime.now() - datetime.timedelta(hours=24 * 360) + datetime.timedelta(hours=hour),
                prediction=random.randint(1000, 3000),
            )
            self.__database.add(db_product)
            self.__database.commit()
            self.__database.refresh(db_product)