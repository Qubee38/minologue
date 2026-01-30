from sqlalchemy import Column, String, Text, Date, Time, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class WorkRecord(Base):
    __tablename__ = "work_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False)
    section_id = Column(UUID(as_uuid=True), ForeignKey("sections.id", ondelete="CASCADE"), nullable=True)
    recorder_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
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
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    field = relationship("Field", back_populates="work_records")
    section = relationship("Section", back_populates="work_records")
    recorder = relationship("User", back_populates="work_records")
    photos = relationship("Photo", back_populates="work_record", cascade="all, delete-orphan")
