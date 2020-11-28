""" Types Models for data between-components transferring.
I tried to use them less because in this specific situation it was easier
 and more operative-memory-friendly. """

from pydantic import BaseModel


class CityData(BaseModel):
    city: str
    start_data: str
    end_data: str

