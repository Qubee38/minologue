from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.api.deps import get_db, get_current_active_user
from app.crud import crud_weather
from app.schemas.weather import WeatherCreate, WeatherResponse
from app.models.user import User

router = APIRouter()


@router.get("", response_model=WeatherResponse)
async def get_weather(
    date: date = Query(..., description="日付"),
    latitude: float = Query(..., ge=-90, le=90, description="緯度"),
    longitude: float = Query(..., ge=-180, le=180, description="経度"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """天候データ取得"""
    weather = await crud_weather.get_by_date_location(
        db,
        date=date,
        latitude=latitude,
        longitude=longitude,
    )
    
    if weather:
        return weather
    
    # Phase 1では気象庁API未実装のため404を返す
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="天候データが見つかりません。手動入力をご利用ください。"
    )


@router.post("", response_model=WeatherResponse, status_code=status.HTTP_201_CREATED)
async def create_weather(
    weather_in: WeatherCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """天候データ手動入力"""
    existing = await crud_weather.get_by_date_location(
        db,
        date=weather_in.date,
        latitude=weather_in.latitude,
        longitude=weather_in.longitude,
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="既に登録されています"
        )
    
    weather = await crud_weather.create(db, obj_in=weather_in)
    return weather
