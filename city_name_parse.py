import os
import json


def load_cities():
    '''Load all cities from /city/city.json to list citiesList'''

    os.chdir("C:\\D\\Programming\\Python\\testing_27_07_22")
    with open('city.json', encoding='utf-8') as f:
        file_content = f.read()
        citiesList = json.loads(file_content)
        return citiesList


def getCityCoordinate(cityName: str):
    '''return (lat,lon) or (None, None)'''
    citiesList = load_cities()
    for city in citiesList:
        if city['city'] == cityName:
            return str(city['geo_lat']), str(city['geo_lon'])
    return None, None
