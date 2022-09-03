import requests

from token_parse import API_TOKEN_WEATHER

from city_name_parse import getCityCoordinate


def get_weather_from_server(lat: str, lon: str):
    url = 'https://api.weather.yandex.ru/v2/informers?lat=' + \
        lat+'&lon='+lon+'&extra=true&lang=ru_RU'
    # url = 'https://api.weather.yandex.ru/v2/informers?lat=55.75396&lon=37.620393&extra=true'
    header = {'X-Yandex-API-Key': API_TOKEN_WEATHER}
    r = requests.get(url, headers=header)
    the_weather = r.json()
    return the_weather


def get_temperature(weather: dict):
    return weather['fact']['temp']


def get_weather(city_name: str):
    lat, lon = getCityCoordinate(city_name)
    if lat and lon:
        weather = get_weather_from_server(lat, lon)
        temperature = get_temperature(weather)
        return temperature
    else:
        return None
