from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from uuid import UUID
from app.crud.base import CRUDBase
from app.models.share import Share
from app.schemas.share import ShareCreate, ShareBase


class CRUDShare(CRUDBase[Share, ShareCreate, ShareBase]):
    async def get_field_shares(
        self, db: AsyncSession, *, field_id: UUID
    ) -> List[Share]:
        """圃場の共有メンバー一覧取得"""
        result = await db.execute(
            select(Share).filter(Share.field_id == field_id)
        )
        return list(result.scalars().all())

    async def get_user_invitations(
        self, db: AsyncSession, *, user_id: UUID
    ) -> List[Share]:
        """ユーザーへの招待一覧取得"""
        result = await db.execute(
            select(Share).filter(
                Share.shared_user_id == user_id,
                Share.status == "pending"
            )
        )
        return list(result.scalars().all())

    async def get_by_field_and_user(
        self, db: AsyncSession, *, field_id: UUID, user_id: UUID
    ) -> Optional[Share]:
        """圃場とユーザーで共有取得"""
        result = await db.execute(
            select(Share).filter(
                Share.field_id == field_id,
                Share.shared_user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def approve(self, db: AsyncSession, *, share_id: UUID) -> Share:
        """招待承認"""
        db_obj = await self.get(db, id=share_id)
        db_obj.status = "approved"
        db_obj.approved_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def reject(self, db: AsyncSession, *, share_id: UUID) -> Share:
        """招待拒否"""
        db_obj = await self.get(db, id=share_id)
        db_obj.status = "rejected"
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_share = CRUDShare(Share)
