from typing import NamedTuple


class Coordinates(NamedTuple):
    latitude: float
    longitude: float

class Temperature(NamedTuple):
    fact_temperature: int
    forecast_temperature: int

class Condition(NamedTuple):
    fact_condition: str
    forecast_condition: str

class WindSpeed(NamedTuple):
    fact_wind_speed: float
    forecast_wind_speed: float