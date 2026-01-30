from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.crud.base import CRUDBase
from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate


class CRUDSection(CRUDBase[Section, SectionCreate, SectionUpdate]):
    async def get_field_sections(
        self, db: AsyncSession, *, field_id: UUID
    ) -> List[Section]:
        """圃場の区画一覧取得"""
        result = await db.execute(
            select(Section)
            .filter(Section.field_id == field_id, Section.is_deleted == False)
            .order_by(Section.display_order)
        )
        return list(result.scalars().all())

    async def create_with_field(
        self, db: AsyncSession, *, obj_in: SectionCreate, field_id: UUID
    ) -> Section:
        """区画作成（圃場ID付き）"""
        db_obj = Section(
            **obj_in.dict(),
            field_id=field_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, db: AsyncSession, *, id: UUID) -> Section:
        """論理削除"""
        db_obj = await self.get(db, id=id)
        db_obj.is_deleted = True
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_section = CRUDSection(Section)
