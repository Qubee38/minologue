from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db, get_current_active_user, check_field_admin
from app.crud.crud_field import crud_field
from app.schemas.field import FieldCreate, FieldUpdate, FieldResponse
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[FieldResponse])
async def get_fields(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """圃場一覧取得"""
    fields = await crud_field.get_user_fields(db, user_id=current_user.id)
    return fields


@router.post("", response_model=FieldResponse, status_code=status.HTTP_201_CREATED)
async def create_field(
    field_in: FieldCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """圃場作成"""
    field = await crud_field.create_with_owner(db, obj_in=field_in, owner_id=current_user.id)
    return field


@router.get("/{field_id}", response_model=FieldResponse)
async def get_field(
    field_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """圃場詳細取得"""
    field = await crud_field.get(db, id=field_id)
    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="圃場が見つかりません"
        )
    return field


@router.put("/{field_id}", response_model=FieldResponse)
async def update_field(
    field_id: int,
    field_in: FieldUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """圃場更新"""
    await check_field_admin(db, field_id, current_user)
    
    field = await crud_field.get(db, id=field_id)
    field = await crud_field.update(db, db_obj=field, obj_in=field_in)
    return field


@router.delete("/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field(
    field_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """圃場削除"""
    field = await crud_field.get(db, id=field_id)
    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="圃場が見つかりません"
        )
    
    # 所有者のみ削除可能
    if field.owner_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="所有者のみ削除できます"
        )
    
    await crud_field.soft_delete(db, id=field_id)
    return None
