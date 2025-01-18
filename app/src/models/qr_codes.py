from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.src.database import Base

import uuid
import datetime

class QrCodes(Base):
    __tablename__ = "qr_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    url = Column(String, index=True)
    color = Column(String, index=True, default="#000000")
    size = Column(Integer, index=True, default=250)
    file_path = Column(String, nullable=False)


    created_at = Column(DateTime, default=func.now()) 
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  
    scan_count = Column(Integer, default=0)


    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship("User", back_populates="qr_codes") 
    scans = relationship("Scans", back_populates="qr_code")
