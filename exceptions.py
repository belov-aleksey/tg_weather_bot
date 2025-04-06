class UnknownCityException(Exception):
    """Для неизвестного города (если введеный пользователем город не содержится в cities.json)"""
    pass

class ServerErrorException(Exception):
    """Для ошибок при обращении по http к Яндекс-Погода"""
    pass