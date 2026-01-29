from pydantic import BaseModel
from typing import List, Generic, TypeVar

DataT = TypeVar('DataT')


class PaginationParams(BaseModel):
    """ページネーションパラメータ"""
    page: int = 1
    per_page: int = 20
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.per_page
    
    @property
    def limit(self) -> int:
        return self.per_page


class PaginationMeta(BaseModel):
    """ページネーションメタ情報"""
    current_page: int
    per_page: int
    total_pages: int
    total_count: int


class PaginatedResponse(BaseModel, Generic[DataT]):
    """ページネーション付きレスポンス"""
    data: List[DataT]
    pagination: PaginationMeta
