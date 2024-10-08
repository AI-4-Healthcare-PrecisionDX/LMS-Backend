from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class Institution(Base):
    institution_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    institution_name = Column(String, nullable=False)
    institution_address = Column(String, nullable=False)
    institution_phone = Column(String, nullable=False)
    institution_email = Column(String, nullable=False)
    institution_website = Column(String, nullable=True)
    institution_fax = Column(String, nullable=True)
    institution_is_active = Column(Boolean(), default=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    branches = relationship("Branch", back_populates="institution")
