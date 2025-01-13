from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base

import uuid

class Scans(Base):
    __tablename__ = "scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    ip = Column(String, index=True)
    timestamp = Column(String, index=True)
    country = Column(String, index=True)
    current_time_from_ip_client = Column(String, index=True)
    city = Column(String, index=True)
    
    qr_uuid = Column(UUID(as_uuid=True), ForeignKey('qr_codes.id', ondelete='CASCADE'))
    qr_code = relationship("QrCodes", back_populates="scans")