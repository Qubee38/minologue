from typing import List, Optional
from datetime import date
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.record import WorkRecord
from app.schemas.record import RecordCreate, RecordUpdate


class CRUDRecord(CRUDBase[WorkRecord, RecordCreate, RecordUpdate]):
    async def get_section_records(
        self,
        db: AsyncSession,
        *,
        section_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        work_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[WorkRecord]:
        """区画の作業記録一覧取得"""
        query = select(WorkRecord).filter(
            WorkRecord.section_id == section_id,
            WorkRecord.is_deleted == False
        )
        
        if start_date:
            query = query.filter(WorkRecord.work_date >= start_date)
        if end_date:
            query = query.filter(WorkRecord.work_date <= end_date)
        if work_type:
            query = query.filter(WorkRecord.work_type == work_type)
        
        query = query.order_by(WorkRecord.work_date.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count_section_records(
        self,
        db: AsyncSession,
        *,
        section_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        work_type: Optional[str] = None
    ) -> int:
        """区画の作業記録件数"""
        query = select(func.count(WorkRecord.id)).filter(
            WorkRecord.section_id == section_id,
            WorkRecord.is_deleted == False
        )
        
        if start_date:
            query = query.filter(WorkRecord.work_date >= start_date)
        if end_date:
            query = query.filter(WorkRecord.work_date <= end_date)
        if work_type:
            query = query.filter(WorkRecord.work_type == work_type)
        
        result = await db.execute(query)
        return result.scalar()

    async def create_with_section(
        self,
        db: AsyncSession,
        *,
        obj_in: RecordCreate,
        section_id: UUID,
        field_id: UUID,  # 追加
        recorder_user_id: UUID
    ) -> WorkRecord:
        """作業記録作成（区画ID付き）"""
        db_obj = WorkRecord(
            **obj_in.model_dump(),
            section_id=section_id,
            field_id=field_id,  # 追加
            recorder_user_id=recorder_user_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, db: AsyncSession, *, id: UUID) -> WorkRecord:
        """論理削除"""
        db_obj = await self.get(db, id=id)
        db_obj.is_deleted = True
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_record = CRUDRecord(WorkRecord)
