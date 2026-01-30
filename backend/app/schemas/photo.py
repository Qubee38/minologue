from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class PhotoBase(BaseModel):
    file_path: str
    file_size: int
    display_order: int


class PhotoCreate(PhotoBase):
    work_record_id: UUID


class Photo(PhotoBase):
    id: UUID
    work_record_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# エイリアス（後方互換性）
PhotoResponse = Photo
