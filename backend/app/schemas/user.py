from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """ユーザー基底スキーマ"""
    email: EmailStr
    display_name: Optional[str] = None
    farm_name: Optional[str] = None


class UserCreate(UserBase):
    """ユーザー作成"""
    password: str


class UserUpdate(BaseModel):
    """ユーザー更新"""
    display_name: Optional[str] = None
    farm_name: Optional[str] = None


class UserResponse(UserBase):
    """ユーザーレスポンス"""
    id: int
    is_active: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """認証トークン"""
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse
