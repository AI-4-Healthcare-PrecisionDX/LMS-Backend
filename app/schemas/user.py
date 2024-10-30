from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.models.teacher import Teacher as TeacherModel


# Shared properties
class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserCreateStudent(UserCreate):
    metric_id: str


class UserCreateTeacher(UserCreate):
    pass


class UserCreateBySuperUser(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    user_id: Optional[UUID] = None
    branch_id: Optional[UUID] = None
    username: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInDBStudent(UserInDBBase):
    student_id: UUID
    metric_id: str


class Student(UserInDBStudent):
    pass


class UserInDBTeacher(UserInDBBase):
    teacher_id: UUID
    pass


class TeacherBase(BaseModel):
    teacher_id: Optional[UUID] = None


class Teacher(UserInDBBase):
    teacher: Optional[TeacherBase] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str
