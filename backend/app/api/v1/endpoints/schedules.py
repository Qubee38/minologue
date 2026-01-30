from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.api.deps import get_db, get_current_active_user, check_field_admin
from app.crud import crud_schedule, crud_section
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from app.models.user import User

router = APIRouter()


@router.get("/sections/{section_id}/schedules", response_model=List[ScheduleResponse])
async def get_section_schedules(
    section_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """区画の年間スケジュール一覧取得"""
    section = await crud_section.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="区画が見つかりません"
        )
    
    schedules = await crud_schedule.get_section_schedules(db, section_id=section_id)
    return schedules


@router.post("/sections/{section_id}/schedules", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    section_id: UUID,
    schedule_in: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """年間スケジュール作成"""
    section = await crud_section.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="区画が見つかりません"
        )
    
    await check_field_admin(db, section.field_id, current_user)
    
    schedule = await crud_schedule.create_with_section(
        db, obj_in=schedule_in, section_id=section_id
    )
    return schedule


@router.put("/schedules/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: UUID,
    schedule_in: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """年間スケジュール更新"""
    schedule = await crud_schedule.get(db, id=schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="スケジュールが見つかりません"
        )
    
    section = await crud_section.get(db, id=schedule.section_id)
    await check_field_admin(db, section.field_id, current_user)
    
    schedule = await crud_schedule.update(db, db_obj=schedule, obj_in=schedule_in)
    return schedule


@router.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """年間スケジュール削除"""
    schedule = await crud_schedule.get(db, id=schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="スケジュールが見つかりません"
        )
    
    section = await crud_section.get(db, id=schedule.section_id)
    await check_field_admin(db, section.field_id, current_user)
    
    await crud_schedule.remove(db, id=schedule_id)
    return None
