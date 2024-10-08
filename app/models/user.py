from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    contact_number = Column(String)
    is_active = Column(Boolean(), default=True)
    role = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)