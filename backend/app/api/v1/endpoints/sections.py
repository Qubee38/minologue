from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.api.deps import get_db, get_current_active_user, check_field_admin, check_field_access
from app.crud.crud_section import crud_section
from app.crud.crud_field import crud_field
from app.schemas.section import SectionCreate, SectionUpdate, SectionResponse
from app.models.user import User

router = APIRouter()


@router.get("/fields/{field_id}/sections", response_model=List[SectionResponse])
async def get_sections(
    field_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """区画一覧取得"""
    await check_field_access(db, field_id, current_user)
    sections = await crud_section.get_field_sections(db, field_id=field_id)
    return sections


@router.post("/fields/{field_id}/sections", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
async def create_section(
    field_id: UUID,
    section_in: SectionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """区画作成"""
    await check_field_admin(db, field_id, current_user)
    section = await crud_section.create_with_field(db, obj_in=section_in, field_id=field_id)
    return section


@router.get("/sections/{section_id}", response_model=SectionResponse)
async def get_section(
    section_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """区画詳細取得"""
    section = await crud_section.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="区画が見つかりません"
        )
    
    await check_field_access(db, section.field_id, current_user)
    return section


@router.put("/sections/{section_id}", response_model=SectionResponse)
async def update_section(
    section_id: UUID,
    section_in: SectionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """区画更新"""
    section = await crud_section.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="区画が見つかりません"
        )
    
    await check_field_admin(db, section.field_id, current_user)
    section = await crud_section.update(db, db_obj=section, obj_in=section_in)
    return section


@router.delete("/sections/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    section_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """区画削除"""
    section = await crud_section.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="区画が見つかりません"
        )
    
    await check_field_admin(db, section.field_id, current_user)
    await crud_section.soft_delete(db, id=section_id)
    return None
