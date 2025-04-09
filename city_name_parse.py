"""
Модуль для парсинга названия города

"""

import os
import json
import sqlite3

from typing import NamedTuple, List, Optional
from loguru import logger

from exceptions import DataBaseException

logger.add('app.log',  format="{time} {level} {message}", level="INFO")

class City(NamedTuple):
    name: str
    subject: str
    district: str
    population: int
    lat: float
    lon: float

class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_city_coordinate(city_name: str) -> Optional[Coordinates]:
    """
    Возвращает координаты объект Coordinates или None 
    
    """
    try:
        with sqlite3.connect('russian_cities.db') as con:
            coordinates = None

            cursor = con.cursor()
            cursor.execute("""
                SELECT lat, lon FROM cities 
                WHERE name = ?
            """, (city_name.title(),))

            result = cursor.fetchone()
            if result:
                coordinates = Coordinates(result[0], result[1])
    except DataBaseException:
        logger.error(f'Ошибка БД при работе с городом {city_name}')
    finally:
        return coordinates

