import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from PIL import Image
import io
import uuid
from app.core.config import settings
from typing import Tuple


# S3クライアント初期化
s3_client = boto3.client(
    's3',
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
    region_name=settings.S3_REGION,
)


async def ensure_bucket_exists():
    """バケット存在確認・作成"""
    try:
        s3_client.head_bucket(Bucket=settings.S3_BUCKET_NAME)
    except ClientError:
        # バケットが存在しない場合は作成
        s3_client.create_bucket(Bucket=settings.S3_BUCKET_NAME)


async def upload_image(file: UploadFile) -> Tuple[str, int]:
    """
    画像アップロード（圧縮処理含む）
    
    Returns:
        Tuple[str, int]: (ファイルパス, ファイルサイズ)
    """
    # ファイル読み込み
    contents = await file.read()
    
    # 画像を開く
    image = Image.open(io.BytesIO(contents))
    
    # EXIF情報に基づいて回転
    try:
        from PIL import ExifTags
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())
        
        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    
    # リサイズ（長辺1920px以下）
    max_size = 1920
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # RGB変換（PNGの透過対応）
    if image.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background
    
    # JPEG圧縮
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=85, optimize=True)
    output.seek(0)
    
    # ファイル名生成
    file_extension = 'jpg'
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"photos/{file_name}"
    
    # S3アップロード
    s3_client.upload_fileobj(
        output,
        settings.S3_BUCKET_NAME,
        file_path,
        ExtraArgs={'ContentType': 'image/jpeg'}
    )
    
    # ファイルサイズ取得
    file_size = output.getbuffer().nbytes
    
    # 完全なURLを返す
    full_path = f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{file_path}"
    
    return full_path, file_size


async def delete_file(file_path: str):
    """ファイル削除"""
    # URLからファイルパスを抽出
    if file_path.startswith('http'):
        # http://minio:9000/minologue-photos/photos/xxx.jpg -> photos/xxx.jpg
        file_path = file_path.split(f"{settings.S3_BUCKET_NAME}/")[-1]
    
    try:
        s3_client.delete_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=file_path
        )
    except ClientError as e:
        print(f"Error deleting file: {e}")
