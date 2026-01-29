from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Section(Base):
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    crop_name = Column(String(100), nullable=False)
    memo = Column(Text, nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # リレーション
    field = relationship("Field", back_populates="sections")
    schedules = relationship("Schedule", back_populates="section", cascade="all, delete-orphan")
    work_records = relationship("WorkRecord", back_populates="section", cascade="all, delete-orphan")
