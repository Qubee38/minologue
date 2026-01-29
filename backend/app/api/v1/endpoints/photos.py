from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_active_user, check_field_access, check_field_admin
from app.crud import crud_photo, crud_record
from app.schemas.photo import PhotoResponse
from app.core.storage import upload_image, delete_file
from app.models.user import User

router = APIRouter()


@router.post("/records/{record_id}/photos", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def upload_photo(
    record_id: int,
    file: UploadFile = File(...),
    display_order: int = Form(..., ge=1, le=2),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """写真アップロード"""
    record = await crud_record.get(db, id=record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作業記録が見つかりません"
        )
    
    await check_field_access(db, record.field_id, current_user)
    
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="画像ファイルのみアップロード可能です"
        )
    
    existing_photos = await crud_photo.get_record_photos(db, work_record_id=record_id)
    if len(existing_photos) >= 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="1つの作業記録には最大2枚まで写真を添付できます"
        )
    
    if any(p.display_order == display_order for p in existing_photos):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"表示順序{display_order}には既に写真が登録されています"
        )
    
    file_path, file_size = await upload_image(file)
    
    photo = await crud_photo.create_with_record(
        db,
        work_record_id=record_id,
        file_path=file_path,
        file_size=file_size,
        display_order=display_order,
    )
    
    return photo


@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """写真削除"""
    photo = await crud_photo.get(db, id=photo_id)
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="写真が見つかりません"
        )
    
    record = await crud_record.get(db, id=photo.work_record_id)
    await check_field_access(db, record.field_id, current_user)
    
    if record.recorder_user_id != current_user.id:
        await check_field_admin(db, record.field_id, current_user)
    
    await delete_file(photo.file_path)
    await crud_photo.remove(db, id=photo_id)
    return None
