# app/crud/crud_course.py
from typing import Any, Dict, Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from app.crud.base import CRUDBase
from app.models.template_course import TemplateCourse
# from app.models.template_course_access import TemplateCourseAccess
from app.models.template_course_materials import CourseMaterials
from app.models.admin import Admin
from app.schemas.course import TemplateCourseCreate, TemplateCourseUpdate
from app.models.teacher import Teacher
from app.crud.crud_user import user
from fastapi import HTTPException
class CRUDTemplateCourse(CRUDBase[TemplateCourse, TemplateCourseCreate, TemplateCourseUpdate]):
    def get_course_by_id(self, db: Session, *, id: UUID) -> Optional[TemplateCourse]:
        return (
            db.query(TemplateCourse)
            .filter(TemplateCourse.template_course_id == id).first()
        )
    
    def get_courses_by_branch_id(self, db: Session, limit:int,skip:int, branch_id: UUID):
        return db.query(TemplateCourse).filter(TemplateCourse.branch_id==branch_id).offset(skip).limit(limit).all()
        
    
    def get_courses_by_department(
        self, db: Session, *, department_id: UUID,
    ) -> List[TemplateCourse]:
        return (
            db.query(TemplateCourse)
            .filter(TemplateCourse.department_id == department_id).all()
        )
    
    def get_admin_by_user_id(self, db: Session, *, user_id: UUID) -> Optional[Admin]:
        return db.query(Admin).filter(Admin.user_id == user_id).first()

    def create_base_course(
        self, db: Session, *, obj_in: TemplateCourseCreate, admin_id: UUID, branch_id: UUID
    ) -> TemplateCourse:
        """Create the base course without materials or access"""
        db_obj = TemplateCourse(
            template_name=obj_in.template_name,
            template_description=obj_in.template_description,
            template_year=obj_in.template_year,
            course_outline=obj_in.course_outline,
            department_id=obj_in.department_id,
            admin_id=admin_id,
            branch_id=branch_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def add_course_access(
    #     self, db: Session, *, template_course_id: UUID, teacher_ids: List[UUID]
    # ) -> None:
    #     """Add teacher access to the course"""
    #     for teacher_id in teacher_ids:
    #         access = TemplateCourseAccess(
    #             template_course_id=template_course_id,
    #             teacher_id=teacher_id,
    #         )
    #         db.add(access)
    #     db.commit()

    def add_course_materials(
        self, db: Session, *, template_course_id: UUID, library_item_ids: List[UUID], user_id: UUID
    ) -> None:
        """Add materials to the course"""
        for library_item_id in library_item_ids:
            material = CourseMaterials(
                template_course_id=template_course_id,
                library_item_id=library_item_id,
                user_id=user_id
            )
            db.add(material)
        db.commit()

    def update_course(
        self,
        db: Session,
        *,
        db_obj: TemplateCourse,
        obj_in: TemplateCourseUpdate | Dict[str, Any],
        user_id: UUID
    ) -> TemplateCourse:
        """
        Update a template course with only the fields provided in obj_in.
        Preserves existing values for fields not included in the update.
        
        Args:
            db: Database session
            db_obj: Existing TemplateCourse object from database
            obj_in: Update data (either Pydantic model or dict)
            user_id: ID of user performing the update
        
        Returns:
            Updated TemplateCourse object
        """
        # Convert input to dictionary if it's a Pydantic model
        if isinstance(obj_in, dict):
            update_data = obj_in.copy()
            library_item_ids = update_data.pop('course_materials', None)
        else:
            update_data = obj_in.model_dump(exclude_unset=True)  # Only get fields that were set
            library_item_ids = update_data.pop('course_materials', None) if 'course_materials' in update_data else None

        # Update only the fields that are present in update_data
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        # Update materials if provided
        if library_item_ids is not None:
            # Delete existing materials
            db.query(CourseMaterials).filter(
                CourseMaterials.template_course_id == db_obj.template_course_id
            ).delete()
            
            # Add new materials
            self.add_course_materials(
                db=db,
                template_course_id=db_obj.template_course_id,
                library_item_ids=library_item_ids,
                user_id=user_id
            )
        
        # Commit changes
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj
    
    def delete_course(self, db: Session, *, id: UUID) -> Dict[str, Any]:
        course = self.get_course_by_id(db=db, id=id)
        if not course:
            raise ValueError("Course not found")
            
        # Delete associated records first
        # db.query(TemplateCourseAccess).filter(
        #     TemplateCourseAccess.template_course_id == id
        # ).delete()
        
        db.query(CourseMaterials).filter(
            CourseMaterials.template_course_id == id
        ).delete()
        
        # Delete the course
        db.delete(course)
        db.commit()
        return {"message": "Course and associated records deleted successfully"}
    
    # def check_if_teacher_has_access(self, db: Session, *, template_course_id: UUID, user_id: UUID) -> bool:
    #     try:
    #         teacher = user.get_teacher_by_user_id(db=db, id=user_id)
    #         if not teacher:
    #             HTTPException(status_code=404, detail="Teacher not found")
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
        
    #     try:
    #         template_course_access = db.query(TemplateCourseAccess).filter(
    #             TemplateCourseAccess.template_course_id == template_course_id,
    #             TemplateCourseAccess.teacher_id == teacher.teacher_id
    #         ).first()
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
        
    #     return True if template_course_access else False
    
    
    
    
template_course = CRUDTemplateCourse(TemplateCourse)