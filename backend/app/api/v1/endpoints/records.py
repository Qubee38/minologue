from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from typing import Optional, List
from datetime import date
from app.api.deps import get_db, get_current_active_user, check_field_access, check_field_admin
from app.crud import crud_record, crud_section
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.models.user import User
from app.models.record import WorkRecord

router = APIRouter()


@router.get("/sections/{section_id}/records")
async def get_section_records(
    section_id: int,
    start_date: Optional[date] = Query(None, description="開始日"),
    end_date: Optional[date] = Query(None, description="終了日"),
    work_type: Optional[str] = Query(None, description="作業種別"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """区画の作業記録一覧取得"""
    section = await crud_section.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="区画が見つかりません"
        )
    
    await check_field_access(db, section.field_id, current_user)
    
    # 写真を含めて明示的にロード
    query = select(WorkRecord).options(selectinload(WorkRecord.photos))
    query = query.filter(
        WorkRecord.section_id == section_id,
        WorkRecord.is_deleted == False
    )
    
    if start_date:
        query = query.filter(WorkRecord.work_date >= start_date)
    if end_date:
        query = query.filter(WorkRecord.work_date <= end_date)
    if work_type:
        query = query.filter(WorkRecord.work_type == work_type)
    
    # ページネーション
    skip = (page - 1) * per_page
    query = query.offset(skip).limit(per_page)
    
    result = await db.execute(query)
    records = list(result.scalars().all())
    
    # 総数カウント
    total = await crud_record.count_section_records(
        db,
        section_id=section_id,
        start_date=start_date,
        end_date=end_date,
        work_type=work_type,
    )
    
    # Pydanticモデルに変換
    record_responses = [
        RecordResponse(
            id=record.id,
            field_id=record.field_id,
            section_id=record.section_id,
            recorder_user_id=record.recorder_user_id,
            record_target=record.record_target,
            work_date=record.work_date,
            start_time=record.start_time,
            end_time=record.end_time,
            work_type=record.work_type,
            custom_work_name=record.custom_work_name,
            quantity=record.quantity,
            quantity_unit=record.quantity_unit,
            memo=record.memo,
            is_deleted=record.is_deleted,
            created_at=record.created_at,
            updated_at=record.updated_at,
            photos=[]  # 一旦空リスト
        )
        for record in records
    ]
    
    return {
        "data": record_responses,
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "total_count": total,
        }
    }


@router.post("/sections/{section_id}/records", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    section_id: int,
    record_in: RecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """作業記録作成"""
    section = await crud_section.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="区画が見つかりません"
        )
    
    await check_field_access(db, section.field_id, current_user)
    
    record = await crud_record.create_with_section(
        db,
        obj_in=record_in,
        section_id=section_id,
        recorder_user_id=current_user.id,
    )
    
    # 作成後に写真を含めて再取得
    query = select(WorkRecord).options(selectinload(WorkRecord.photos))
    query = query.filter(WorkRecord.id == record.id)
    result = await db.execute(query)
    record_with_photos = result.scalar_one()
    
    return RecordResponse(
        id=record_with_photos.id,
        field_id=record_with_photos.field_id,
        section_id=record_with_photos.section_id,
        recorder_user_id=record_with_photos.recorder_user_id,
        record_target=record_with_photos.record_target,
        work_date=record_with_photos.work_date,
        start_time=record_with_photos.start_time,
        end_time=record_with_photos.end_time,
        work_type=record_with_photos.work_type,
        custom_work_name=record_with_photos.custom_work_name,
        quantity=record_with_photos.quantity,
        quantity_unit=record_with_photos.quantity_unit,
        memo=record_with_photos.memo,
        is_deleted=record_with_photos.is_deleted,
        created_at=record_with_photos.created_at,
        updated_at=record_with_photos.updated_at,
        photos=[]
    )


@router.get("/records/{record_id}", response_model=RecordResponse)
async def get_record(
    record_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """作業記録詳細取得"""
    query = select(WorkRecord).options(selectinload(WorkRecord.photos))
    query = query.filter(WorkRecord.id == record_id)
    result = await db.execute(query)
    record = result.scalar_one_or_none()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作業記録が見つかりません"
        )
    
    await check_field_access(db, record.field_id, current_user)
    
    return RecordResponse(
        id=record.id,
        field_id=record.field_id,
        section_id=record.section_id,
        recorder_user_id=record.recorder_user_id,
        record_target=record.record_target,
        work_date=record.work_date,
        start_time=record.start_time,
        end_time=record.end_time,
        work_type=record.work_type,
        custom_work_name=record.custom_work_name,
        quantity=record.quantity,
        quantity_unit=record.quantity_unit,
        memo=record.memo,
        is_deleted=record.is_deleted,
        created_at=record.created_at,
        updated_at=record.updated_at,
        photos=[]
    )


@router.put("/records/{record_id}", response_model=RecordResponse)
async def update_record(
    record_id: int,
    record_in: RecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """作業記録更新"""
    record = await crud_record.get(db, id=record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作業記録が見つかりません"
        )
    
    await check_field_access(db, record.field_id, current_user)
    
    if record.recorder_user_id != current_user.id:
        await check_field_admin(db, record.field_id, current_user)
    
    record = await crud_record.update(db, db_obj=record, obj_in=record_in)
    
    # 更新後に写真を含めて再取得
    query = select(WorkRecord).options(selectinload(WorkRecord.photos))
    query = query.filter(WorkRecord.id == record.id)
    result = await db.execute(query)
    record_with_photos = result.scalar_one()
    
    return RecordResponse(
        id=record_with_photos.id,
        field_id=record_with_photos.field_id,
        section_id=record_with_photos.section_id,
        recorder_user_id=record_with_photos.recorder_user_id,
        record_target=record_with_photos.record_target,
        work_date=record_with_photos.work_date,
        start_time=record_with_photos.start_time,
        end_time=record_with_photos.end_time,
        work_type=record_with_photos.work_type,
        custom_work_name=record_with_photos.custom_work_name,
        quantity=record_with_photos.quantity,
        quantity_unit=record_with_photos.quantity_unit,
        memo=record_with_photos.memo,
        is_deleted=record_with_photos.is_deleted,
        created_at=record_with_photos.created_at,
        updated_at=record_with_photos.updated_at,
        photos=[]
    )


@router.delete("/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    record_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """作業記録削除"""
    record = await crud_record.get(db, id=record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作業記録が見つかりません"
        )
    
    await check_field_access(db, record.field_id, current_user)
    
    if record.recorder_user_id != current_user.id:
        await check_field_admin(db, record.field_id, current_user)
    
    await crud_record.soft_delete(db, id=record_id)
    return None
