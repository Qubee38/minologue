from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API設定
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Minologue"
    VERSION: str = "1.0.0"
    
    # セキュリティ
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # データベース
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # MinIO/S3 (既存コードとの互換性を保つ)
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_BUCKET_NAME: str = "minologue"
    S3_REGION: str = "us-east-1"
    
    # 既存コードとの互換性のためのプロパティ
    @property
    def S3_ENDPOINT(self) -> str:
        return self.S3_ENDPOINT_URL
    
    @property
    def S3_ACCESS_KEY(self) -> str:
        return self.S3_ACCESS_KEY_ID
    
    @property
    def S3_SECRET_KEY(self) -> str:
        return self.S3_SECRET_ACCESS_KEY
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # デバッグ
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
