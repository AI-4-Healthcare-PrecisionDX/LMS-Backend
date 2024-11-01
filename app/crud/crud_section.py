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
from app.schemas.section import SectionCreate, SectionUpdate
from app.crud.crud_user import user
class CRUDSection(CRUDBase[Section, SectionCreate, SectionUpdate]):
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
        # Get the course
        course = db.query(TemplateCourse).filter(
            TemplateCourse.template_course_id == template_course_id
        ).first()
        
        if not course:
            raise ValueError("Course not found")

        # Generate base code from course name
        course_name = course.template_name.upper()
        words = course_name.split()
        if len(words) >= 2:
            base_code = f"{words[0][:3]}{words[1][:3]}"
        else:
            base_code = words[0][:6]
        
        # Clean the base code (remove special characters)
        base_code = ''.join(c for c in base_code if c.isalnum())

        # Get number of existing sections for this course
        existing_sections_count = (
            db.query(func.count(Section.section_id))
            .filter(Section.template_course_id == template_course_id)
            .scalar()
        )
        
        # Generate the full section code
        section_code = f"{base_code}-{str(existing_sections_count + 1).zfill(2)}"
        
        # Verify uniqueness and try alternatives if needed
        counter = 1
        original_code = section_code
        while db.query(Section).filter(Section.section_code == section_code).first():
            counter += 1
            section_code = f"{original_code}-{counter}"
        
        return section_code

    def get_section_by_id(self, db: Session, *, id: UUID) -> Optional[Section]:
        """Get section by ID with related information"""
        
        try:
            section = (
                db.query(Section)
                .filter(Section.section_id == id).first()
            )
            if not section:
                raise ValueError("Section not found")
            
        except Exception as e:
            raise ValueError(f"An error occurred while retrieving section: {str(e)}")
        
        return section

    def get_sections_by_teacher(
        self, db: Session, *, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Section]:
        """Get all sections for a specific teacher"""
        
        try:
            teacher = user.get_teacher_by_user_id(db=db, id=user_id)
            if not teacher:
                raise ValueError("Teacher not found")
        except Exception as e:
            raise ValueError(f"An error occurred while retrieving teacher: {str(e)}")
        
        return (
            db.query(Section)
            .filter(Section.teacher_id == teacher.teacher_id).all()
        )

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
    ) -> Section:
        """Create a new section with auto-generated section code"""
        # Get teacher record from user_id
        teacher = user.get_teacher_by_user_id(db=db, id=user_id)
        # Check if teacher has access to the course
        # accessible_courses = self.get_teacher_course_access(db=db, teacher_id=teacher.teacher_id)
        # if obj_in.template_course_id not in accessible_courses:
        #     raise ValueError("Teacher does not have access to this course")
        
        # Generate section code
        section_code = self.generate_section_code(db, obj_in.template_course_id)
        
        # Create section with auto-generated code
        db_obj = Section(
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
        
        # Return section with related data
        return self.get_section_by_id(db=db, id=db_obj.section_id)

    def update_section(
        self, 
        db: Session, 
        *, 
        db_obj: Section,
        obj_in: SectionUpdate | Dict[str, Any],
        teacher_id: UUID
    ) -> Section:
        """Update a section"""
        # Get teacher record from user_id
        teacher = self.get_teacher_by_user_id(db=db, user_id=teacher_id)
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
        teacher = self.get_teacher_by_user_id(db=db, user_id=teacher_id)
        if not teacher:
            return False

        section = self.get_section_by_id(db=db, id=section_id)
        if not section:
            return False

        return section.teacher_id == teacher.teacher_id

section = CRUDSection(Section)