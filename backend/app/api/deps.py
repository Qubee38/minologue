from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.crud import crud_user, crud_field, crud_share
from app.models.user import User
from app.models.field import Field

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_db() -> Generator:
    """データベースセッションを取得"""
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """現在のユーザーを取得"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報を検証できませんでした",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # 文字列のuser_idを整数に変換
        user_id_int = int(user_id)
        
    except (JWTError, ValueError):
        raise credentials_exception
    
    user = await crud_user.get(db, id=user_id_int)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """アクティブなユーザーを取得"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="アクティブでないユーザーです"
        )
    return current_user


async def check_field_access(
    db: AsyncSession,
    field_id: int,
    current_user: User
) -> Field:
    """圃場へのアクセス権限をチェック（閲覧権限）"""
    field = await crud_field.get(db, id=field_id)
    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="圃場が見つかりません"
        )
    
    # 所有者チェック
    if field.owner_user_id == current_user.id:
        return field
    
    # 共有メンバーチェック
    share = await crud_share.get_by_field_and_user(
        db, field_id=field_id, user_id=current_user.id
    )
    if share and share.status == "approved":
        return field
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="この圃場へのアクセス権限がありません"
    )


async def check_field_admin(
    db: AsyncSession,
    field_id: int,
    current_user: User
) -> Field:
    """圃場への管理者権限をチェック"""
    field = await crud_field.get(db, id=field_id)
    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="圃場が見つかりません"
        )
    
    # 所有者チェック
    if field.owner_user_id == current_user.id:
        return field
    
    # 管理者権限の共有メンバーチェック
    share = await crud_share.get_by_field_and_user(
        db, field_id=field_id, user_id=current_user.id
    )
    if share and share.status == "approved" and share.role == "admin":
        return field
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="この圃場への管理者権限がありません"
    )
