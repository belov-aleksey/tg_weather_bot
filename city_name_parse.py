"""
Модуль для парсинга названия города

"""

import os
import json

from typing import NamedTuple

from exceptions import UnknownCityException


class Coordinates(NamedTuple):
    latitude: float
    longitude: float

def load_cities() -> list:
    """
    Загружает имена всех городов из city.json в массив citiesList, 
    элементы которых dict с данными о городах
    
    """
    with open('city.json', encoding='utf-8') as f:
        file_content = f.read()
        cities_list = json.loads(file_content)
        return cities_list

def get_city_coordinate(city_name: str) -> Coordinates:
    """
    Возвращает координаты  (lat,lon) or (None, None) по названию города
    
    """
    citiesList = load_cities()
    for city in citiesList:
        if city['city'].lower() == city_name.lower():
            return Coordinates(latitude=city['geo_lat'], longitude=city['geo_lon'])
    raise UnknownCityException