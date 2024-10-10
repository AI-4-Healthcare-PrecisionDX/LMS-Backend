from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


# Default settings
DEFAULT_NOTIFICATION_PREFERENCE = {"email": True, "sms": False, "push": True}

DEFAULT_PRIVACY_PREFERENCE = {"profile_visible": True, "searchable": False}


# setting_id, notification_preference, privacy_preference, account_status, updated_at, created_at
class UserSettings(Base):
    __tablename__ = "user_settings"

    settings_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    notification_preference = Column(
        JSON, nullable=False, default=DEFAULT_NOTIFICATION_PREFERENCE
    )
    privacy_preference = Column(
        JSON, nullable=False, default=DEFAULT_PRIVACY_PREFERENCE
    )
    account_status = Column(Boolean(), default=True)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    user = relationship("User", back_populates="settings")
