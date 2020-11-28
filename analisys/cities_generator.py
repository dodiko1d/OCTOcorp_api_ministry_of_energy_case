from city import City
from sqlalchemy.orm import Session


class CitiesGenerator:
    """ Cities database generator. """

    __cities_list = [
        'Чебоксары',
    ]

    def __init__(self, database: Session) -> None:
        self.__database = database
        self.__generate()

    def __generate_city(self, name: str) -> None:
        city = City(
            name=name,
        )
        self.__database.add(city)
        self.__database.commit()
        self.__database.refresh(city)

    def __generate(self) -> None:
        for city_name in CitiesGenerator.__cities_list:
            self.__generate_city(city_name)
