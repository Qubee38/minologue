from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.crud.base import CRUDBase
from app.models.photo import Photo
from app.schemas.photo import PhotoBase, PhotoResponse


class CRUDPhoto(CRUDBase[Photo, PhotoBase, PhotoBase]):
    async def get_record_photos(
        self, db: AsyncSession, *, work_record_id: UUID
    ) -> List[Photo]:
        """作業記録の写真一覧取得"""
        result = await db.execute(
            select(Photo)
            .filter(Photo.work_record_id == work_record_id)
            .order_by(Photo.display_order)
        )
        return list(result.scalars().all())

    async def create_with_record(
        self,
        db: AsyncSession,
        *,
        work_record_id: UUID,
        file_path: str,
        file_size: int,
        display_order: int
    ) -> Photo:
        """写真作成（作業記録ID付き）"""
        db_obj = Photo(
            work_record_id=work_record_id,
            file_path=file_path,
            file_size=file_size,
            display_order=display_order
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_photo = CRUDPhoto(Photo)
