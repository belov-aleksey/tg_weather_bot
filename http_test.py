import requests
from parse import API_TOKEN_WEATHER


def get_weather():
    url = 'https://api.weather.yandex.ru/v2/forecast?lat=55.75396&lon=37.620393&extra=false&lang=ru_RU'
    header = {'X-Yandex-API-Key': API_TOKEN_WEATHER}
    r = requests.get(url, headers=header)
    the_weather = r.json()

    return the_weather


print(get_weather()['info']['tzinfo']['name'])
print(get_weather()['geo_object']['district']['name'])

print(get_weather()['fact']['temp'])
