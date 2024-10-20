from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime
from fastapi import UploadFile, File


# Shared properties
class LibraryBase(BaseModel):
    material_type: Optional[str] = None
    material_title: Optional[str] = None
    material_description: Optional[str] = None
    author: Optional[str] = None
    visibility: Optional[bool] = True


# Properties to receive via API on creation
class LibraryCreate(LibraryBase):
    material_type: str
    material_title: str
    material_description: Optional[str] = None


class LibraryUpdate(LibraryBase):
    pass


class LibraryInDBBase(LibraryBase):
    library_id: Optional[UUID] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    user_id: Optional[UUID] = None


class Library(LibraryInDBBase):
    pass
