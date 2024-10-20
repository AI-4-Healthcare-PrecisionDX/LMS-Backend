from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate
from app.models.teacher import Teacher
from app.models.admin import Admin

import uuid


class CRUDSection(CRUDBase[Section, SectionCreate, SectionUpdate]):
    
    def get_section_by_id(self, db: Session, *, id: str) -> Optional[Section]:
        return db.query(Section).filter(Section.section_id == id).first()

    def get_multi(self, db, *, skip=0, limit=100):
        return super().get_multi(db, skip=skip, limit=limit)
    
    def create_section(self, db: Session, *, obj_in: SectionCreate, teacher_id: uuid) -> Section:
        print(f"Teacher ID: {teacher_id}")
        # Ensure that the user creating the section is a teacher
        teacher = db.query(Teacher).filter(Teacher.user_id == teacher_id).first()
        #teacher = db.query(Teacher).filter_by(teacher_id=teacher_id).first()
        #teacher = db.query(Teacher).get(teacher_id)


        print(f"Teacher ID2 : {teacher}")
        if not teacher:
            raise ValueError("User is not authorized to create sections")
        
        db_obj = Section(
            section_name=obj_in.section_name,
            section_code=obj_in.section_code,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            teacher_id=teacher.teacher_id,
            template_course_id=obj_in.template_course_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_section(
        self, db: Session, *, db_obj: Section, obj_in: SectionUpdate | Dict[str, Any], teacher_id: uuid
    ) -> Section:
        teacher = db.query(Teacher).filter(Teacher.user_id == teacher_id).first()
        # Ensure that the user updating the section is the same teacher
        if db_obj.teacher_id != teacher.teacher_id:
            raise ValueError("User is not authorized to update this section")
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete_section(self, db: Session, *, id: str) -> Dict[str, Any]:
        section = db.query(Section).filter(Section.section_id == id).first()
        if section is None:
            raise ValueError("Section not found")
        
        db.delete(section)
        db.commit()
        return {"message": "Section deleted successfully"}


section = CRUDSection(Section)
