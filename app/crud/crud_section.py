# app/crud/crud_section.py
from typing import Any, Dict, Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from uuid import UUID
import random
import string

from app.crud.base import CRUDBase
from app.models.section import Section
from app.models.student_stats import StudentStats
from app.models.teacher import Teacher
from app.models.template_course import TemplateCourse
from app.models.template_course_access import TemplateCourseAccess
from app.models.section import Section
from app.models.section_exclusive_content import SectionExclusiveContent
from app.schemas.section import (
    Section,
    SectionCreate,
    SectionUpdate,
    SectionExclusiveContentCreate,
    SectionExclusiveContentInDB
)
from app.models.section import Section as SectionModel
from app.schemas.section import Section as SectionSchema

from app.crud.crud_user import user
class CRUDSection(CRUDBase[SectionModel, SectionCreate, SectionUpdate]):
    def get_teacher_course_access(self, db: Session, *, teacher_id: UUID) -> List[UUID]:
        """Get all course IDs that the teacher has access to"""
        course_access = (
            db.query(TemplateCourseAccess.template_course_id)
            .filter(TemplateCourseAccess.teacher_id == teacher_id)
            .all()
        )
        return [access[0] for access in course_access]

    def generate_section_code(self, db: Session, template_course_id: UUID) -> str:
        """Generate a unique section code based on course"""
        course = db.query(TemplateCourse).filter(
            TemplateCourse.template_course_id == template_course_id
        ).first()
        
        if not course:
            raise ValueError("Course not found")

        course_name = course.template_name.upper()
        words = course_name.split()
        if len(words) >= 2:
            base_code = f"{words[0][:3]}{words[1][:3]}"
        else:
            base_code = words[0][:6]
        
        base_code = ''.join(c for c in base_code if c.isalnum())

        existing_sections_count = (
            db.query(func.count(SectionModel.section_id))
            .filter(SectionModel.template_course_id == template_course_id)
            .scalar()
        )
        
        section_code = f"{base_code}-{str(existing_sections_count + 1).zfill(2)}"
        
        counter = 1
        original_code = section_code
        while db.query(SectionModel).filter(SectionModel.section_code == section_code).first():
            counter += 1
            section_code = f"{original_code}-{counter}"
        
        return section_code

    def get_section_by_id(self, db: Session, *, id: UUID) -> Optional[SectionModel]:
        """Get section by ID with all related data including exclusive contents"""
        return (
            db.query(SectionModel)
            .filter(SectionModel.section_id == id)
            .options(
                joinedload(SectionModel.teacher).joinedload(Teacher.user),
                joinedload(SectionModel.template_course),
                joinedload(SectionModel.section_exclusive_contents).joinedload(SectionExclusiveContent.library_item)
            )
            .first()
        )

    def get_sections_by_teacher(
        self, db: Session, *, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[SectionModel]:
        """Get all sections for a teacher with all related data"""
        teacher = user.get_teacher_by_user_id(db=db, id=user_id)
        if not teacher:
            return []
            
        return (
            db.query(SectionModel)
            .filter(SectionModel.teacher_id == teacher.teacher_id)
            .options(
                joinedload(SectionModel.teacher).joinedload(Teacher.user),
                joinedload(SectionModel.template_course),
                joinedload(SectionModel.section_exclusive_contents).joinedload(SectionExclusiveContent.library_item)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def check_section_owner(
        self, db: Session, *, section_id: UUID, teacher_id: UUID
    ) -> bool:
        section = (
            db.query(Section)
            .filter(
                Section.section_id == section_id,
                Section.teacher_id == teacher_id
            )
            .first()
        )
        return bool(section)

    # def get_teacher_by_user_id(self, db: Session, *, user_id: UUID) -> Optional[Teacher]:
    #     """Get teacher record from user_id"""
    #     return (
    #         db.query(Teacher)
    #         .filter(Teacher.user_id == user_id)
    #         .options(joinedload(Teacher.user))
    #         .first()
    #     )

    def create_section(
        self, db: Session, *, obj_in: SectionCreate, user_id: UUID
    ) -> SectionModel:
        """Create a new section with auto-generated section code"""
        teacher = user.get_teacher_by_user_id(db=db, id=user_id)
        if not teacher:
            raise ValueError("Teacher not found")
            
        section_code = self.generate_section_code(db, obj_in.template_course_id)
        
        db_obj = SectionModel(
            section_name=obj_in.section_name,
            section_code=section_code,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            template_course_id=obj_in.template_course_id,
            teacher_id=teacher.teacher_id
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return self.get_section_by_id(db=db, id=db_obj.section_id)

    def update_section(
        self, 
        db: Session, 
        *, 
        db_obj: Section,
        obj_in: SectionUpdate | Dict[str, Any],
        user_id: UUID
    ) -> Section:
        """Update a section"""
        # Get teacher record from user_id
        teacher = user.get_teacher_by_user_id(db=db, id=user_id)
        if not teacher:
            raise ValueError("Teacher not found")

        # Verify teacher owns the section
        if db_obj.teacher_id != teacher.teacher_id:
            raise ValueError("Teacher does not have permission to update this section")

        if isinstance(obj_in, dict):
            update_data = obj_in.copy()
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # If template_course_id is being updated, verify teacher has access
        if 'template_course_id' in update_data:
            accessible_courses = self.get_teacher_course_access(db=db, teacher_id=teacher.teacher_id)
            if update_data['template_course_id'] not in accessible_courses:
                raise ValueError("Teacher does not have access to the target course")

        # Update section (section_code is never included in update_data)
        updated_obj = super().update(db, db_obj=db_obj, obj_in=update_data)
        
        # Return updated section with related data
        return self.get_section_by_id(db=db, id=updated_obj.section_id)

    def delete_section(self, db: Session, *, id: UUID) -> Dict[str, Any]:
        """Delete a section and its related records"""
        section = self.get_section_by_id(db=db, id=id)
        if not section:
            raise ValueError("Section not found")

        # Delete related records first
        db.query(StudentStats).filter(StudentStats.section_id == id).delete()
        
        # Delete the section
        db.delete(section)
        db.commit()
        
        return {"message": "Section and related records deleted successfully"}

    def check_section_owner(
        self, db: Session, *, section_id: UUID, teacher_id: UUID
    ) -> bool:
        """Check if the teacher owns the section"""
        teacher = user.get_teacher_by_user_id(db=db, id=teacher_id)
        if not teacher:
            return False

        section = self.get_section_by_id(db=db, id=section_id)
        if not section:
            return False

        return section.teacher_id == teacher.teacher_id
    
    
    def get_section_contents(
        self,
        db: Session,
        *,
        section_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[SectionExclusiveContent]:
        """Get all exclusive contents for a specific section with pagination"""
        return (
            db.query(SectionExclusiveContent)
            .filter(SectionExclusiveContent.section_id == section_id)
            .options(joinedload(SectionExclusiveContent.library_item))  # Eager load library item details
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def add_exclusive_content(
        self, 
        db: Session, 
        *, 
        section_id: UUID,
        user_id: UUID,
        library_item_id: UUID
    ) -> Optional[SectionExclusiveContent]:
        # Check if content already exists
        existing_content = (
            db.query(SectionExclusiveContent)
            .filter(
                SectionExclusiveContent.section_id == section_id,
                SectionExclusiveContent.library_item_id == library_item_id
            )
            .first()
        )
        if existing_content:
            raise ValueError("This content is already added to the section")
            
        db_obj = SectionExclusiveContent(
            section_id=section_id,
            library_item_id=library_item_id,
            user_id=user_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    def remove_exclusive_content(
        self,
        db: Session,
        *,
        section_id: UUID,
        library_item_id: UUID
    ) -> bool:
        content = (
            db.query(SectionExclusiveContent)
            .filter(
                SectionExclusiveContent.section_id == section_id,
                SectionExclusiveContent.library_item_id == library_item_id
            )
            .first()
        )
        if not content:
            return False
        db.delete(content)
        db.commit()
        return True




section = CRUDSection(Section)