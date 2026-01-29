from sqlalchemy import Column, BigInteger, String, Date, Numeric, Boolean, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base


class WeatherData(Base):
    """天候データモデル"""
    __tablename__ = "weather_data"
    
    id = Column(BigInteger, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    location_text = Column(String(200), nullable=False)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    weather = Column(String(50), nullable=False)
    max_temperature = Column(Numeric(4, 1), nullable=True)
    min_temperature = Column(Numeric(4, 1), nullable=True)
    precipitation = Column(Numeric(5, 1), nullable=True)
    wind_speed = Column(Numeric(4, 1), nullable=True)
    is_manual = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # 制約
    __table_args__ = (
        CheckConstraint("weather IN ('晴れ', '曇り', '雨', '雪', '台風')", name='check_weather'),
        CheckConstraint('latitude >= -90 AND latitude <= 90', name='check_latitude'),
        CheckConstraint('longitude >= -180 AND longitude <= 180', name='check_longitude'),
        UniqueConstraint('date', 'latitude', 'longitude', name='uq_date_location'),
    )