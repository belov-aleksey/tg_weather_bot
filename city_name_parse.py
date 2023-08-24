'''
Модуль для парсинга названия города
load_cities - загружает 
'''

import os
import json


def load_cities():
    '''
    Загружает имена всех городов из city.json в массив citiesList, 
    элементы которых dict с данными о городах
    '''
    with open('city.json', encoding='utf-8') as f:
        file_content = f.read()
        cities_list = json.loads(file_content)
        return cities_list


def get_city_coordinate(city_name: str):
    '''
    Возвращает координаты  (lat,lon) or (None, None) по названию города
    '''
    citiesList = load_cities()
    for city in citiesList:
        if city['city'].lower() == city_name.lower():
            return str(city['geo_lat']), str(city['geo_lon'])
    return None, None
