from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    fields,
    sections,
    schedules,
    records,
    photos,
    shares,
    dashboard,
    weather,
)

api_router = APIRouter()

# 認証
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# ユーザー
api_router.include_router(users.router, prefix="/users", tags=["users"])

# 圃場
api_router.include_router(fields.router, prefix="/fields", tags=["fields"])

# 区画
api_router.include_router(sections.router, tags=["sections"])

# 年間スケジュール
api_router.include_router(schedules.router, tags=["schedules"])

# 作業記録
api_router.include_router(records.router, tags=["records"])

# 写真
api_router.include_router(photos.router, tags=["photos"])

# 共有
api_router.include_router(shares.router, tags=["shares"])

# ダッシュボード
api_router.include_router(dashboard.router, tags=["dashboard"])

# 天候
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
