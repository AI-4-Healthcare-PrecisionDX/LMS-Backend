# app/models/user.py

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


# user_id, first_name, last_name, email, password, gender, phone_number, role, is_active, updated_at, created_at
class User(Base):
    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    role = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    branch_id = Column(UUID(as_uuid=True), ForeignKey("branch.branch_id"))
    branch = relationship("Branch", back_populates="users")

    settings = relationship(
        "UserSettings", back_populates="user", uselist=False
    )  # One to One relationship
    admin = relationship(
        "Admin", back_populates="user", uselist=False
    )  # One to One relationship
    teacher = relationship(
        "Teacher", back_populates="user", uselist=False
    )  # One to One relationship
    student = relationship(
        "Student", back_populates="user", uselist=False
    )  # One to One relationship

    global_library_items = relationship("GlobalLibrary", back_populates="user")

    course_materials = relationship("CourseMaterials", back_populates="user")

    discussion_messages = relationship("DiscussionMessage", back_populates="user")

    discussion_reply_messages = relationship(
        "DiscussionReplyMessage", back_populates="user"
    )
