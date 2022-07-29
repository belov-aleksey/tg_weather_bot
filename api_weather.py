import requests
from parse import API_TOKEN_WEATHER

from city import getCityCoordinate


def get_weather_from_server(lat: str, lon: str):
    url = 'https://api.weather.yandex.ru/v2/forecast?lat=' + \
        lat+'&lon='+lon+'&extra=false&lang=ru_RU'
    header = {'X-Yandex-API-Key': API_TOKEN_WEATHER}
    r = requests.get(url, headers=header)
    the_weather = r.json()
    return the_weather


def get_temperature(weather: dict):
    return weather['fact']['temp']


def get_city_name(weather: dict):
    return weather['geo_object']['locality']['name']


def get_weather(city_name: str):
    lat, lon = getCityCoordinate(city_name)
    weather = get_weather_from_server(lat, lon)
    temperature = get_temperature(weather)
    city = get_city_name(weather)
    return city, temperature
