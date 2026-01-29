from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FieldBase(BaseModel):
    """圃場基底スキーマ"""
    name: str
    location_text: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    memo: Optional[str] = None


class FieldCreate(FieldBase):
    """圃場作成"""
    pass


class FieldUpdate(BaseModel):
    """圃場更新"""
    name: Optional[str] = None
    location_text: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    memo: Optional[str] = None


class FieldResponse(FieldBase):
    """圃場レスポンス"""
    id: int
    owner_user_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
