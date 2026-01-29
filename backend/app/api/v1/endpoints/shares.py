from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db, get_current_active_user, check_field_admin
from app.crud import crud_share, crud_user
from app.schemas.share import ShareCreate, ShareResponse
from app.models.user import User

router = APIRouter()


@router.get("/users/me/invitations", response_model=List[ShareResponse])
async def get_my_invitations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """自分への招待一覧取得"""
    shares = await crud_share.get_user_invitations(db, user_id=current_user.id)
    return shares


@router.get("/fields/{field_id}/shares", response_model=List[ShareResponse])
async def get_field_shares(
    field_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """圃場の共有メンバー一覧取得"""
    await check_field_admin(db, field_id, current_user)
    shares = await crud_share.get_field_shares(db, field_id=field_id)
    return shares


@router.post("/fields/{field_id}/shares", response_model=ShareResponse, status_code=status.HTTP_201_CREATED)
async def create_share(
    field_id: int,
    share_in: ShareCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """メンバー招待"""
    await check_field_admin(db, field_id, current_user)
    
    invited_user = await crud_user.get_by_email(db, email=share_in.email)
    if not invited_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="登録されていないユーザーです"
        )
    
    existing_share = await crud_share.get_by_field_and_user(
        db, field_id=field_id, user_id=invited_user.id
    )
    if existing_share:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="既に招待済みのユーザーです"
        )
    
    share = await crud_share.create(
        db,
        obj_in={
            "field_id": field_id,
            "shared_user_id": invited_user.id,
            "role": share_in.role,
            "status": "pending",
            "invited_by_user_id": current_user.id,
        }
    )
    
    return share


@router.patch("/shares/{share_id}/approve", response_model=ShareResponse)
async def approve_share(
    share_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """招待承認"""
    share = await crud_share.get(db, id=share_id)
    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="招待が見つかりません"
        )
    
    if share.shared_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="自分への招待のみ承認できます"
        )
    
    share = await crud_share.approve(db, share_id=share_id)
    return share


@router.patch("/shares/{share_id}/reject", response_model=ShareResponse)
async def reject_share(
    share_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """招待拒否"""
    share = await crud_share.get(db, id=share_id)
    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="招待が見つかりません"
        )
    
    if share.shared_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="自分への招待のみ拒否できます"
        )
    
    share = await crud_share.reject(db, share_id=share_id)
    return share


@router.delete("/shares/{share_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_share(
    share_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """共有メンバー削除"""
    share = await crud_share.get(db, id=share_id)
    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="共有が見つかりません"
        )
    
    await check_field_admin(db, share.field_id, current_user)
    await crud_share.remove(db, id=share_id)
    return None
