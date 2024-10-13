from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.template_course import TemplateCourse
from app.schemas.course import TemplateCourseCreate, TemplateCourseUpdate
from app.models.branch import Branch
from app.schemas.super_admin import BranchCreate, BranchUpdate
from app.models.department import Department
from app.schemas.super_admin import DepartmentCreate, DepartmentUpdate
from app.models.admin import Admin

import uuid


class CRUDCourse(CRUDBase[TemplateCourse, TemplateCourseCreate, TemplateCourseUpdate]):
    def get_course_by_id(self, db: Session, *, id: str) -> Optional[TemplateCourse]:
        return db.query(TemplateCourse).filter(TemplateCourse.template_course_id == id).first()

    def get_multi(self, db, *, skip = 0, limit = 100):
        return super().get_multi(db, skip=skip, limit=limit)
    
    def create_course(self, db: Session, *, obj_in: TemplateCourseCreate,admin_id : uuid) -> TemplateCourse:
        db_obj = TemplateCourse(
            template_name=obj_in.template_name,
            template_description=obj_in.template_description,
            template_year=obj_in.template_year,
            course_outline=obj_in.course_outline,
            admin_id = admin_id,
            department_id = obj_in.department_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_course(
        self, db: Session, *, db_obj: TemplateCourse, obj_in: TemplateCourseUpdate | Dict[str, Any], admin_id: uuid
    ) -> TemplateCourse:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        # Update the admin_id
        update_data['admin_id'] = admin_id

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete_course(self, db: Session, *, id: str) -> Dict[str, Any]:
        course = db.query(TemplateCourse).filter(TemplateCourse.template_course_id == id).first()
        if course is None:
            raise ValueError("Course not found")
        
        db.delete(course)
        db.commit()
        return {"message": "Course deleted successfully"}
    
    def get_admin_by_user_id(self, db: Session, *, user_id: uuid) -> uuid:
        return db.query(Admin).filter(Admin.user_id == user_id).first()


    

course = CRUDCourse(TemplateCourse)