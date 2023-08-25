'''
Загружает телеграм-токен и яндекс погода - токен в переменные 
API_TOKEN_TG, API_TOKEN_WEATHER 

'''
import os

from dotenv import load_dotenv


load_dotenv()
API_TOKEN_TG = os.getenv('TG_TOKEN')
API_TOKEN_WEATHER = os.getenv('YANDEX_WEATHER_TOKEN')
