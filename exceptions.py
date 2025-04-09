class ServerErrorException(Exception):
    """Для ошибок при обращении по http к Яндекс-Погода"""
    pass

class DataBaseException(Exception):
    """Для ошибок при запросе к БД"""
    pass