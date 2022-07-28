import requests
from parse import API_TOKEN_WEATHER

from city import getCityCoordinate

lat, lon = getCityCoordinate('Санкт-Петербург')

'''lat = '53.1950306'
lon = '50.1069518'''


def get_weather():
    url = 'https://api.weather.yandex.ru/v2/forecast?lat=' + \
        lat+'&lon='+lon+'&extra=false&lang=ru_RU'
    header = {'X-Yandex-API-Key': API_TOKEN_WEATHER}
    r = requests.get(url, headers=header)
    the_weather = r.json()

    return the_weather


print(get_weather()['info']['tzinfo']['name'])
print(get_weather()['fact']['temp'])
print(get_weather()['geo_object'])
