from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID


class ShareBase(BaseModel):
    role: str = "recorder"


class ShareCreate(BaseModel):
    email: EmailStr
    role: str = "recorder"


class ShareUpdate(BaseModel):
    role: str | None = None
    status: str | None = None


class Share(ShareBase):
    id: UUID
    field_id: UUID
    shared_user_id: UUID
    status: str
    invited_by_user_id: UUID
    created_at: datetime
    updated_at: datetime
    approved_at: datetime | None = None

    class Config:
        from_attributes = True


ShareResponse = Share