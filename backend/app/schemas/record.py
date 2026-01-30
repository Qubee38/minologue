from pydantic import BaseModel
from datetime import date, time, datetime
from uuid import UUID


class WorkRecordBase(BaseModel):
    work_date: date
    start_time: time
    end_time: time
    work_type: str
    custom_work_name: str | None = None
    quantity: float | None = None
    quantity_unit: str | None = None
    memo: str | None = None
    record_target: str = "section"


class WorkRecordCreate(WorkRecordBase):
    pass


class WorkRecordUpdate(WorkRecordBase):
    work_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    work_type: str | None = None


class PhotoResponse(BaseModel):
    id: UUID
    file_path: str
    file_size: int
    display_order: int
    created_at: datetime

    class Config:
        from_attributes = True


class RecordResponse(WorkRecordBase):
    id: UUID
    field_id: UUID
    section_id: UUID | None
    recorder_user_id: UUID
    photos: list[PhotoResponse] = []
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkRecord(RecordResponse):
    pass


# 後方互換性のためのエイリアス
RecordCreate = WorkRecordCreate
RecordUpdate = WorkRecordUpdate