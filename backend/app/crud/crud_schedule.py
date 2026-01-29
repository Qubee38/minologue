from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    async def get_section_schedules(
        self, db: AsyncSession, *, section_id: int
    ) -> List[Schedule]:
        """区画の年間スケジュール取得"""
        result = await db.execute(
            select(Schedule)
            .filter(Schedule.section_id == section_id)
            .order_by(Schedule.month)
        )
        return list(result.scalars().all())

    async def create_with_section(
        self, db: AsyncSession, *, obj_in: ScheduleCreate, section_id: int
    ) -> Schedule:
        """年間スケジュール作成（区画ID付き）"""
        db_obj = Schedule(
            **obj_in.dict(),
            section_id=section_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_schedule = CRUDSchedule(Schedule)
