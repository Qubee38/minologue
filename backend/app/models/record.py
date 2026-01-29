from sqlalchemy import Column, Integer, String, Float, Text, Boolean, Date, Time, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class WorkRecord(Base):
    __tablename__ = "work_records"
    
    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id", ondelete="CASCADE"), nullable=True)
    recorder_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    record_target = Column(String(20), default="section", nullable=False)
    work_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    work_type = Column(String(50), nullable=False)
    custom_work_name = Column(String(100), nullable=True)
    quantity = Column(Float, nullable=True)
    quantity_unit = Column(String(20), nullable=True)
    memo = Column(Text, nullable=True)
    edit_history = Column(JSON, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # リレーション
    field = relationship("Field", back_populates="work_records")
    section = relationship("Section", back_populates="work_records")
    recorder = relationship("User", back_populates="work_records", foreign_keys=[recorder_user_id])
    photos = relationship("Photo", back_populates="work_record", cascade="all, delete-orphan")
