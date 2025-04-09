"""
Получение данных о погоде по API от Яндекс-Погода.

На момент написания комментария (апрель 2025) используется v2 версия API
на тарифе "Погода на вашем сайте".

В ответ на запрос приходит JSON. 
Подробнее о формате на https://yandex.ru/dev/weather/doc/ru/concepts/forecast-info#resp-format
"""

from loguru import logger

from aiohttp import ClientSession

from db import get_city_coordinates 
from exceptions import ServerErrorException
from settings import API_TOKEN_WEATHER, URL_API_YANDEX
from models import Coordinates, Temperature, Condition, WindSpeed

logger.add('app.log',  format="{time} {level} {message}", level="INFO")

RU_CONDITIONS = {
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

RU_PART_NAMES = {
    "night": "ночь",
    "day": "день",
    "evening": "вечер",
    "morning": "утро"
}


async def get_weather_from_server(coordinates: Coordinates) -> dict:
    """
    Возвращает данные о погоде в словаре weather

    """
    url = f'{URL_API_YANDEX}?lat={coordinates.latitude}&lon={coordinates.longitude}&extra=true&lang=ru_RU'
    headers = {'X-Yandex-API-Key': API_TOKEN_WEATHER}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise ServerErrorException
            else:
                return await response.json()


def get_tempereture(weather: dict) -> Temperature:
    """
    Возвращает значение температуры 
    fact_temperature - температура воздуха в настоящее время
    forecast_temperature - прогноз температуры погоды в ближайшее время

    """
    fact_temperature = weather['fact']['temp']
    forecast_temperature = weather['forecast']['parts'][0]['temp_avg']
    return Temperature(fact_temperature, forecast_temperature)


def get_condition(weather: dict) -> Condition:
    """
    Возвращает значение температуры 
    fact_temperature - температура воздуха в настоящее время
    forecast_temperature - прогноз температуры погоды в ближайшее время

    """
    fact_condition = RU_CONDITIONS[weather['fact']['condition']]
    forecast_condition = RU_CONDITIONS[weather['forecast']['parts'][0]['condition']]
    return Condition(fact_condition, forecast_condition)


def get_wind_speed(weather: dict) -> WindSpeed:
    """
    Возвращает значение скорости ветра
    fact_wind - скорость ветра в настоящее время
    forecast_wind - прогноз скорости ветра в ближайшее время

    """   
    fact_wind_speed = str(weather['fact']['wind_speed'])
    forecast_wind_speed = str(weather['forecast']['parts'][0]['wind_speed'])
    return WindSpeed(fact_wind_speed, forecast_wind_speed)


def get_forecast_part_name(weather: dict) -> str:
    """
    Возвращает строку с названием предстоящего времени суток (утро, день, вечер, ночь)

    """
    return RU_PART_NAMES[weather['forecast']['parts'][0]['part_name']]

def parse_weather(weather: dict, city_name: str) -> str:
    temperature = get_tempereture(weather)
    wind_speed = get_wind_speed(weather)
    condition = get_condition(weather)
    forecast_part_name = get_forecast_part_name(weather)
    answer = f'Город: {city_name.capitalize()}. По данным Яндекс-Погода: \n\n' \
        f'Температура воздуха: {temperature.fact_temperature}, {condition.fact_condition}\n' \
        f'Скорость ветра: {wind_speed.fact_wind_speed} \n\n'\
        '----------------\n\n' \
        f'Прогноз погоды на {forecast_part_name}:\n' \
        f'Температура воздуха: {temperature.forecast_temperature}, {condition.forecast_condition}\n' \
        f'Скорость ветра: {wind_speed.forecast_wind_speed}'
    return answer

def get_api_error() -> str:
    return 'Сервер недоступен. Попробуйте позже'

def get_unknown_city_error() -> str:
    return 'Информации о погоде в этом городе нет. \n\n' \
            'Проверьте правильность написания названия города '\
            'и повторите попытку снова. Например: Нижний Новгород'

async def get_weather(city_name: str) -> str:
    """
    Формирует ответ пользователю. Если данные о погоде по введеному названию городу получены,
    то возвращается строка с данными о текущей погоде и прогнозе погоде. Если данных нет,
    то возращается строка с текстом об ошибке
    
    """
    coordinates = None
    logger.info(f'Начинаю поиск координат города {city_name}')

    coordinates = get_city_coordinates(city_name)

    if not coordinates:
        answer = get_unknown_city_error()
        logger.info(f'Неизвестный город {city_name}')   
    else:
        logger.info(f'Для города {city_name} найдены координаты: {coordinates.latitude}, {coordinates.longitude}')

        try:
            logger.info(f'Отправляю запрос на сервер по городу {city_name}')
            weather = await get_weather_from_server(coordinates)
            logger.info(f'Данные по городу {city_name} получены')
            answer = parse_weather(weather, city_name)
        except ServerErrorException:
            answer =  get_api_error() 
            logger.error(f'Сервер не дал ответ по городу {city_name}')
    return answer        
