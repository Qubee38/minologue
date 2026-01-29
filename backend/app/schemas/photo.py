from pydantic import BaseModel, Field
from datetime import datetime


class PhotoBase(BaseModel):
    """写真基底スキーマ"""
    display_order: int = Field(..., ge=1, le=2, description="表示順序（1 or 2）")


class PhotoResponse(PhotoBase):
    """写真レスポンス"""
    id: int
    work_record_id: int
    file_path: str
    file_size: int
    created_at: datetime
    
    class Config:
        from_attributes = True
