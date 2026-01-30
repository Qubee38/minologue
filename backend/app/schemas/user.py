from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr
    display_name: str | None = None
    farm_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    display_name: str | None = None
    farm_name: str | None = None


class User(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None

    class Config:
        from_attributes = True


class UserInDB(User):
    password_hash: str


# エイリアス（後方互換性）
UserResponse = User


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse  # ユーザー情報を含める


class TokenData(BaseModel):
    user_id: UUID | None = None
