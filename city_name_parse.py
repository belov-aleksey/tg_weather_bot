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
    Загружает имена всех городов из cities.json в список cities, 
    элементы которых dict с данными о городах
    
    """
    with open('cities.json', encoding='utf-8') as f:
        file_content = f.read()
        cities = json.loads(file_content)
        return cities

def get_city_coordinate(city_name: str) -> Coordinates:
    """
    Возвращает координаты  (lat,lon) or (None, None) по названию города
    
    """
    cities = load_cities()
    for city in cities:
        if city['city'].lower() == city_name.lower():
            return Coordinates(latitude=city['geo_lat'], longitude=city['geo_lon'])
    raise UnknownCityException