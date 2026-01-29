from pydantic import BaseModel
from typing import Optional, Literal, List
from datetime import date, time, datetime


class RecordBase(BaseModel):
    """作業記録基底スキーマ"""
    record_target: Literal["section", "field"] = "section"
    work_date: date
    start_time: time
    end_time: time
    work_type: str
    custom_work_name: Optional[str] = None
    quantity: Optional[float] = None
    quantity_unit: Optional[str] = None
    memo: Optional[str] = None


class RecordCreate(RecordBase):
    """作業記録作成"""
    pass


class RecordUpdate(BaseModel):
    """作業記録更新"""
    work_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    work_type: Optional[str] = None
    custom_work_name: Optional[str] = None
    quantity: Optional[float] = None
    quantity_unit: Optional[str] = None
    memo: Optional[str] = None


class PhotoResponse(BaseModel):
    """写真レスポンス"""
    id: int
    file_path: str
    file_size: int
    display_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RecordResponse(RecordBase):
    """作業記録レスポンス"""
    id: int
    field_id: int
    section_id: Optional[int] = None
    recorder_user_id: int
    photos: List[PhotoResponse] = []
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
