from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class FieldBase(BaseModel):
    name: str
    location_text: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    memo: str | None = None


class FieldCreate(FieldBase):
    pass


class FieldUpdate(FieldBase):
    name: str | None = None


class Field(FieldBase):
    id: UUID
    owner_user_id: UUID
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FieldWithSections(Field):
    sections_count: int = 0


# エイリアス（後方互換性）
FieldResponse = Field