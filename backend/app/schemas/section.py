from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class SectionBase(BaseModel):
    name: str
    crop_name: str
    memo: str | None = None
    display_order: int = 0


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    name: str | None = None
    crop_name: str | None = None


class Section(SectionBase):
    id: UUID
    field_id: UUID
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


SectionResponse = Section