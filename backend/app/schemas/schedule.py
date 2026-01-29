from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ScheduleBase(BaseModel):
    """年間スケジュール基底スキーマ"""
    month: int = Field(..., ge=1, le=12, description="月（1-12）")
    work_content: str = Field(..., max_length=200, description="作業内容")


class ScheduleCreate(ScheduleBase):
    """年間スケジュール作成"""
    pass


class ScheduleUpdate(BaseModel):
    """年間スケジュール更新"""
    month: Optional[int] = Field(None, ge=1, le=12)
    work_content: Optional[str] = Field(None, max_length=200)


class ScheduleResponse(ScheduleBase):
    """年間スケジュールレスポンス"""
    id: int
    section_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
