from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SectionBase(BaseModel):
    """区画基底スキーマ"""
    name: str
    crop_name: str
    memo: Optional[str] = None
    display_order: int = 0


class SectionCreate(SectionBase):
    """区画作成"""
    pass


class SectionUpdate(BaseModel):
    """区画更新"""
    name: Optional[str] = None
    crop_name: Optional[str] = None
    memo: Optional[str] = None
    display_order: Optional[int] = None


class SectionResponse(SectionBase):
    """区画レスポンス"""
    id: int
    field_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
