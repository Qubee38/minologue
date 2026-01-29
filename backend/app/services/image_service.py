from PIL import Image
import io
from app.core.config import settings


class ImageService:
    """画像処理サービス"""
    
    def compress_image(self, image_data: bytes) -> bytes:
        """画像圧縮"""
        image = Image.open(io.BytesIO(image_data))
        
        # RGB変換
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # リサイズ
        max_dim = settings.IMAGE_MAX_DIMENSION
        width, height = image.size
        
        if width > max_dim or height > max_dim:
            if width > height:
                new_width = max_dim
                new_height = int(height * (max_dim / width))
            else:
                new_height = max_dim
                new_width = int(width * (max_dim / height))
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # JPEG圧縮
        output = io.BytesIO()
        image.save(
            output,
            format='JPEG',
            quality=settings.IMAGE_JPEG_QUALITY,
            optimize=True
        )
        
        return output.getvalue()


image_service = ImageService()