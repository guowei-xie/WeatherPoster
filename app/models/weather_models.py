from pydantic import BaseModel
from typing import List

class Weather(BaseModel):
    main: str
    description: str
    icon: str

class MainData(BaseModel):
    temp: float
    feels_like: float
    humidity: int

class Wind(BaseModel):
    speed: float

class WeatherData(BaseModel):
    name: str
    weather: List[Weather]
    main: MainData
    wind: Wind