from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID


class WeatherBase(BaseModel):
    date: date
    location_text: str
    latitude: float
    longitude: float
    weather: str
    max_temperature: float | None = None
    min_temperature: float | None = None
    precipitation: float | None = None
    wind_speed: float | None = None
    is_manual: bool = False


class WeatherCreate(WeatherBase):
    pass


class WeatherUpdate(BaseModel):
    weather: str | None = None
    max_temperature: float | None = None
    min_temperature: float | None = None
    precipitation: float | None = None
    wind_speed: float | None = None


class Weather(WeatherBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


WeatherResponse = Weather