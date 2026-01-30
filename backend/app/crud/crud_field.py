from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.crud.base import CRUDBase
from app.models.field import Field
from app.models.share import Share
from app.schemas.field import FieldCreate, FieldUpdate


class CRUDField(CRUDBase[Field, FieldCreate, FieldUpdate]):
    async def get_user_fields(
        self, 
        db: AsyncSession, 
        user_id: UUID
    ) -> List[Field]:
        """ユーザーの圃場一覧を取得（所有＋共有）"""
        # 所有している圃場を取得
        owned_result = await db.execute(
            select(Field).filter(
                Field.owner_user_id == user_id,
                Field.is_deleted == False
            )
        )
        owned_fields = list(owned_result.scalars().all())
        
        # 共有されている圃場を取得
        shared_result = await db.execute(
            select(Field).join(Share).filter(
                Share.shared_user_id == user_id,
                Share.status == "approved",
                Field.is_deleted == False
            )
        )
        shared_fields = list(shared_result.scalars().all())
        
        # 重複を除いてマージ（IDベース）
        field_dict = {}
        for field in owned_fields + shared_fields:
            if field.id not in field_dict:
                field_dict[field.id] = field
        
        return list(field_dict.values())
    
    async def create_with_owner(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: FieldCreate, 
        owner_id: UUID
    ) -> Field:
        """圃場を作成（所有者付き）"""
        db_obj = Field(
            owner_user_id=owner_id,
            **obj_in.model_dump()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def soft_delete(
        self, 
        db: AsyncSession, 
        *, 
        db_obj: Field
    ) -> Field:
        """圃場を論理削除"""
        db_obj.is_deleted = True
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_field = CRUDField(Field)
