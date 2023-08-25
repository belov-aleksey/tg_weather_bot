"""
Получение данных о погоде по API от Яндекс-Погода

"""

from aiohttp import ClientSession
from typing import NamedTuple

from settings import API_TOKEN_WEATHER  # Загрузка токена для запроса по API к Яндекс-Погода
from city_name_parse import get_city_coordinate 
from exceptions import ServerErrorException, UnknownCityException
from city_name_parse import Coordinates


class Temperature(NamedTuple):
    fact_temperature: int
    forecast_temperature: int

RU_CONDITION = {
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

RU_PART_NAME = {
    "night": "ночь",
    "day": "день",
    "evening": "вечер",
    "morning": "утро"
}


async def get_weather_from_server(Coordinates) -> dict:
    """
    Возвращает данные о погоде в словаре weather

    """
    lat = str(Coordinates.latitude)
    lon = str(Coordinates.longitude)
    url = f'https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}&extra=true&lang=ru_RU'
    headers = {'X-Yandex-API-Key': API_TOKEN_WEATHER}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise ServerErrorException
            else:
                return await response.json()


def get_tempereture(weather:dict) -> Temperature:
    """
    Возвращает значение температуры 
    fact_temperature - температура воздуха в настоящее время
    forecast_temperature - прогноз температуры погоды в ближайшее время

    """
    fact_temperature = weather['fact']['temp']
    forecast_temperature = weather['forecast']['parts'][0]['temp_avg']
    return Temperature(fact_temperature=fact_temperature, forecast_temperature=forecast_temperature)


def get_condition(weather: dict) -> (str, str):
    """
    Возвращает значение температуры 
    fact_temperature - температура воздуха в настоящее время
    forecast_temperature - прогноз температуры погоды в ближайшее время

    """
    fact_condition = RU_CONDITION[weather['fact']['condition']]
    forecast_condition = RU_CONDITION[weather['forecast']['parts'][0]['condition']]
    return fact_condition, forecast_condition


def get_wind_speed(weather: dict) -> (str, str):
    """
    Возвращает значение скорости ветра
    fact_wind - скорость ветра в настоящее время
    forecast_wind - прогноз скорости ветра в ближайшее время

    """   
    fact_wind = str(weather['fact']['wind_speed'])
    forecast_wind = str(weather['forecast']['parts'][0]['wind_speed'])
    return fact_wind, forecast_wind


def get_forecast_part_name(weather: dict) -> str:
    """
    Возвращает строку с названием предстоящего времени суток (утро, день, вечер, ночь)

    """
    return RU_PART_NAME[weather['forecast']['parts'][0]['part_name']]


async def get_weather(city_name:str) -> str:
    """
    Формирует ответ пользователю. Если данные о погоде по введеному названию городу получены,
    то возвращается строка с данными о текущей погоде и прогнозе погоде. Если данных нет,
    то возращается строка с текстом об ошибке
    
    """
    try:
        coordinates = get_city_coordinate(city_name)
    except UnknownCityException:
        answer = 'Информации о погоде в этом городе нет. \n\n' \
        'Проверьте правильность написания названия города '\
        'и повторите попытку снова. Например: Нижний Новгород'
        coordinates = False
    if coordinates:
        try:
            weather = await get_weather_from_server(coordinates)
        except ServerErrorException:
                answer = 'Сервер недоступен. Попробуйте позже'
        fact_temperature, forecast_temperature = get_tempereture(weather)
        fact_wind, forecast_wind = get_wind_speed(weather)
        fact_condition, forecast_condition = get_condition(weather)
        forecast_part_name = get_forecast_part_name(weather)
        answer = f'Город: {city_name.capitalize()}. По данным Яндекс-Погода: \n\n' \
            f'Температура воздуха: {fact_temperature}, {fact_condition}\n' \
            f'Скорость ветра: {fact_wind} \n\n'\
            '----------------\n\n' \
            f'Прогноз погоды на {forecast_part_name}:\n' \
            f'Температура воздуха: {forecast_temperature}, {forecast_condition}\n' \
            f'Скорость ветра: {forecast_wind}' 
         
    return answer        
