from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ScheduleBase(BaseModel):
    month: int
    work_content: str


class ScheduleCreate(ScheduleBase):
    section_id: UUID


class ScheduleUpdate(BaseModel):
    month: int | None = None
    work_content: str | None = None


class Schedule(ScheduleBase):
    id: UUID
    section_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


ScheduleResponse = Schedule