from sqlalchemy import Column, BigInteger, String, Integer, SmallInteger, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Photo(Base):
    """写真モデル"""
    __tablename__ = "photos"
    
    id = Column(BigInteger, primary_key=True, index=True)
    work_record_id = Column(BigInteger, ForeignKey("work_records.id", ondelete="CASCADE"), nullable=False, index=True)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    display_order = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # 制約
    __table_args__ = (
        CheckConstraint('display_order >= 1 AND display_order <= 2', name='check_display_order'),
        CheckConstraint('file_size <= 2097152', name='check_file_size'),  # 2MB
        UniqueConstraint('work_record_id', 'display_order', name='uq_work_record_display_order'),
    )
    
    # リレーション
    work_record = relationship("WorkRecord", back_populates="photos")