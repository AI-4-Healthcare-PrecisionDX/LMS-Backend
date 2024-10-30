from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime
from .user import User


# For Departments
class DepartmentBase(BaseModel):
    department_name: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    department_name: str


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentInDBBase(DepartmentBase):
    department_id: Optional[UUID] = None
    branch_id: Optional[UUID] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Department(DepartmentInDBBase):
    pass


# For Branches
class BranchBase(BaseModel):
    branch_name: Optional[str] = None
    branch_address: Optional[str] = None
    branch_contact: Optional[str] = None
    branch_email: Optional[str] = None
    branch_website: Optional[str] = None
    branch_fax: Optional[str] = None


class BranchCreate(BranchBase):
    branch_name: str
    branch_address: str
    branch_contact: str
    branch_email: str


class BranchUpdate(BranchBase):
    branch_is_active: Optional[bool] = None
    pass


class BranchInDBBase(BranchBase):
    branch_id: Optional[UUID] = None
    branch_is_active: Optional[bool] = True
    institution_id: Optional[UUID] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Branch(BranchInDBBase):
    pass


# For Institutions
class InstitutionBase(BaseModel):
    institution_name: Optional[str] = None
    institution_address: Optional[str] = None
    institution_phone: Optional[str] = None
    institution_email: Optional[str] = None
    institution_website: Optional[str] = None
    institution_fax: Optional[str] = None


class InstitutionCreate(InstitutionBase):
    institution_name: str
    institution_address: str
    institution_phone: str
    institution_email: str


class InstitutionUpdate(InstitutionBase):
    institution_is_active: Optional[bool] = None
    pass


class InstitutionInDBBase(InstitutionBase):
    institution_id: Optional[UUID] = None
    institution_is_active: Optional[bool] = True
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Institution(InstitutionInDBBase):
    pass
