from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date, datetime


class WeatherBase(BaseModel):
    """天候基底スキーマ"""
    date: datetime = Field(..., description="日付")
    location_text: str = Field(..., max_length=200, description="観測地点名")
    latitude: float = Field(..., ge=-90, le=90, description="緯度")
    longitude: float = Field(..., ge=-180, le=180, description="経度")
    weather: Literal["晴れ", "曇り", "雨", "雪", "台風"] = Field(..., description="天候")
    max_temperature: Optional[float] = Field(None, description="最高気温（℃）")
    min_temperature: Optional[float] = Field(None, description="最低気温（℃）")
    precipitation: Optional[float] = Field(None, ge=0, description="降水量（mm）")
    wind_speed: Optional[float] = Field(None, ge=0, description="風速（m/s）")


class WeatherCreate(WeatherBase):
    """天候データ作成（手動入力）"""
    pass


class WeatherResponse(WeatherBase):
    """天候データレスポンス"""
    id: int
    is_manual: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
