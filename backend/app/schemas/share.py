from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime


class ShareBase(BaseModel):
    """共有基底スキーマ"""
    role: Literal["admin", "recorder"] = Field(..., description="役割")


class ShareCreate(BaseModel):
    """共有作成（招待）"""
    email: EmailStr = Field(..., description="招待するユーザーのメールアドレス")
    role: Literal["admin", "recorder"] = Field(..., description="役割")


class ShareResponse(ShareBase):
    """共有レスポンス"""
    id: int
    field_id: int
    shared_user_id: int
    status: Literal["pending", "approved", "rejected"]
    invited_by_user_id: int
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
