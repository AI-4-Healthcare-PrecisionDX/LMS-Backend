from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.institution import Institution
from app.schemas.super_admin import InstitutionCreate, InstitutionUpdate
from app.models.branch import Branch
from app.schemas.super_admin import BranchCreate, BranchUpdate
from app.models.department import Department
from app.schemas.super_admin import DepartmentCreate, DepartmentUpdate
import uuid


class CRUDInstitution(CRUDBase[Institution, InstitutionCreate, InstitutionUpdate]):
    def get_institution_by_id(self, db: Session, *, id: str) -> Optional[Institution]:
        return db.query(Institution).filter(Institution.institution_id == id).first()

    def get_institution_by_email(
        self, db: Session, *, email: str
    ) -> Optional[Institution]:
        return db.query(Institution).filter(Institution.email == email).first()

    def create_institution(
        self, db: Session, *, obj_in: InstitutionCreate
    ) -> Institution:
        db_obj = Institution(
            institution_name=obj_in.institution_name,
            institution_address=obj_in.institution_address,
            institution_phone=obj_in.institution_phone,
            institution_email=obj_in.institution_email,
            institution_website=obj_in.institution_website,
            institution_fax=obj_in.institution_fax,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_institution(
        self,
        db: Session,
        *,
        db_obj: Institution,
        obj_in: InstitutionUpdate | Dict[str, Any]
    ) -> Institution:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete_institution(self, db: Session, *, id: str) -> Institution:
        institution = (
            db.query(Institution).filter(Institution.institution_id == id).first()
        )
        db.delete(institution)
        db.commit()
        return institution


class CRUDBranch(CRUDBase[Branch, BranchCreate, BranchUpdate]):
    def get_branch_by_id(self, db: Session, *, id: str) -> Optional[Branch]:
        return db.query(Branch).filter(Branch.branch_id == id).first()

    def get_branch_by_email(self, db: Session, *, email: str) -> Optional[Branch]:
        return db.query(Branch).filter(Branch.email == email).first()

    def create_branch(self, db: Session, *, obj_in: BranchCreate) -> Branch:
        db_obj = Branch(
            branch_name=obj_in.branch_name,
            branch_address=obj_in.branch_address,
            branch_contact=obj_in.branch_contact,
            branch_email=obj_in.branch_email,
            branch_website=obj_in.branch_website,
            branch_fax=obj_in.branch_fax,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_branch(
        self, db: Session, *, db_obj: Branch, obj_in: BranchUpdate | Dict[str, Any]
    ) -> Branch:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete_branch(self, db: Session, *, id: str) -> Branch:
        branch = db.query(Branch).filter(Branch.branch_id == id).first()
        db.delete(branch)
        db.commit()
        return branch


class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    def get_department_by_id(self, db: Session, *, id: str) -> Optional[Department]:
        return db.query(Department).filter(Department.department_id == id).first()

    def get_department_by_email(
        self, db: Session, *, email: str
    ) -> Optional[Department]:
        return db.query(Department).filter(Department.email == email).first()

    def create_department(self, db: Session, *, obj_in: DepartmentCreate) -> Department:
        db_obj = Department(
            department_name=obj_in.department_name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_department(
        self,
        db: Session,
        *,
        db_obj: Department,
        obj_in: DepartmentUpdate | Dict[str, Any]
    ) -> Department:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete_department(self, db: Session, *, id: str) -> Department:
        department = db.query(Department).filter(Department.department_id == id).first()
        db.delete(department)
        db.commit()
        return department


institution = CRUDInstitution(Institution)
branch = CRUDBranch(Branch)
department = CRUDDepartment(Department)
