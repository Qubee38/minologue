from typing import Optional
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.weather import WeatherData
from app.schemas.weather import WeatherCreate, WeatherBase


class CRUDWeather(CRUDBase[WeatherData, WeatherCreate, WeatherBase]):
    async def get_by_date_location(
        self,
        db: AsyncSession,
        *,
        date: date,
        latitude: float,
        longitude: float
    ) -> Optional[WeatherData]:
        """日付・位置で天候データ取得"""
        result = await db.execute(
            select(WeatherData).filter(
                WeatherData.date == date,
                WeatherData.latitude == latitude,
                WeatherData.longitude == longitude
            )
        )
        return result.scalar_one_or_none()


crud_weather = CRUDWeather(WeatherData)
