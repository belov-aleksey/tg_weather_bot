import requests

from token_parse import API_TOKEN_WEATHER

from city_name_parse import getCityCoordinate

ru_cond = {
    'clear': 'ясно',
    'partly-cloudy': 'малооблачно',
    'cloudy': 'облачно с прояснениями',
    'overcast': 'пасмурно',
    'drizzle': 'морось',
    'light-rain': 'небольшой дождь',
    'rain': 'дождь',
    'moderate-rain': 'умеренно сильный дождь',
    'heavy-rain': 'сильный дождь',
    'continuous-heavy-rain': 'длительный сильный дождь',
    'showers': 'ливень',
    'wet-snow': 'дождь со снегом',
    'light-snow': 'небольшой снег',
    'snow': 'снег',
    'snow-showers': 'снегопад',
    'hail': 'град',
    'thunderstorm': 'гроза',
    'thunderstorm-with-rain': 'дождь с грозой',
    'thunderstorm-with-hail': 'гроза с градом'
}


ru_part_name = {
    "night": "ночь",
    "day": "день",
    "evening": "вечер",
    "morning": "утро"
}


def get_weather_from_server(lat: str, lon: str) -> dict:
    url = 'https://api.weather.yandex.ru/v2/informers?lat=' + \
        lat+'&lon='+lon+'&extra=true&lang=ru_RU'
    # url = 'https://api.weather.yandex.ru/v2/informers?lat=55.75396&lon=37.620393&extra=true'
    header = {'X-Yandex-API-Key': API_TOKEN_WEATHER}
    r = requests.get(url, headers=header)
    weather = r.json()
    return weather


def get_fact_temp(weather: dict) -> str:
    return str(weather['fact']['temp'])


def get_fact_condition(weather: dict) -> str:
    return ru_cond[weather['fact']['condition']]


def get_fact_wind_speed(weather: dict) -> str:
    return str(weather['fact']['wind_speed'])


def get_forecast_part_name(weather: dict) -> str:
    return ru_part_name[weather['forecast']['parts'][1]['part_name']]


def get_forecast_temp(weather: dict) -> str:
    return str(weather['forecast']['parts'][0]['temp_avg'])


def get_forecast_condition(weather: dict) -> str:
    return ru_cond[weather['forecast']['parts'][0]['condition']]


def get_forecast_wind(weather: dict) -> str:
    return weather['forecast']['parts'][0]['wind_speed']


def get_fact_weather(city_name: str) -> str:
    lat, lon = getCityCoordinate(city_name)
    if lat and lon:
        weather = get_weather_from_server(lat, lon)
        temp = get_fact_temp(weather)
        cond = get_fact_condition(weather)
        wind = get_fact_wind_speed(weather)
        ans = city_name + "\nПо данным Яндекс.Погода\n"\
            + "Температура воздуха: " + temp + ", " + cond + "\n"\
            + "Скорость ветра: " + wind
        return ans
    else:
        ans = """Информации о погоде в этом городе нет.
        Проверьте правильность написания названия города
        и повторите попытку снова. Например: Нижний Новгород"""
        return ans


def get_forecast_weather(city_name: str) -> str:
    lat, lon = getCityCoordinate(city_name)
    if lat and lon:
        weather = get_weather_from_server(lat, lon)
        part_name = get_forecast_part_name(weather)
        temp = get_forecast_temp(weather)
        cond = get_forecast_condition(weather)
        wind = get_fact_wind_speed(weather)
        ans = "Прогноз по данным Яндекс.Погода\n"\
            + "Город: " + city_name + "\n"\
            + "Время суток: " + part_name + "\n"\
            + "Температура воздуха: " + temp + ", " + cond + "\n"\
            + "Скорость ветра: " + wind
        return ans
    else:
        ans = """Информации о погоде в этом городе нет.
        Проверьте правильность написания названия города
        и повторите попытку снова. Например: Нижний Новгород"""
        return ans


# print(getCityCoordinate("Самара"))
#w = get_weather_from_server('53', '50')
# print(get_fact_weather('Самара'))
# print(get_forecast_weather('Самара'))
# print('')
