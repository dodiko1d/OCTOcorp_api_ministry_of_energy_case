import requests


class APIConnector:
    def get_city_weather_now(self, city: str) -> list:
        api_key = 'b7c64d93c03bdae1a2a5afb7da027d6a'
        response = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                params={
                                    'q': city,
                                    'units': 'metric',
                                    'lang': 'ru',
                                    'APPID': api_key
                                }
                                )
        data = response.json()
        return data

#    def get_power_consumption(self):




