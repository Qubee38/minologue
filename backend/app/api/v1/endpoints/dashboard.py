from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_active_user, check_field_access
from app.crud import crud_section
from app.models.user import User

router = APIRouter()


@router.get("/sections/{section_id}/dashboard")
async def get_dashboard_data(
    section_id: int,
    year: int = Query(..., description="年"),
    month: int = Query(..., ge=1, le=12, description="月"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """ダッシュボードデータ取得"""
    section = await crud_section.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="区画が見つかりません"
        )
    
    await check_field_access(db, section.field_id, current_user)
    
    # 簡易版：実際のデータ集計は後で実装
    return {
        "section": {
            "id": section.id,
            "name": section.name,
            "crop_name": section.crop_name,
        },
        "period": {
            "year": year,
            "month": month,
        },
        "summary": {
            "total_work_time": 0,
            "total_water": 0,
            "total_fertilizer": 0,
            "total_pesticide": 0,
            "total_harvest": 0,
        },
        "daily_data": [],
    }
