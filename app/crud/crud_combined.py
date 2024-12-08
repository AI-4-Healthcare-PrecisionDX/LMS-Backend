from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.section import Section as SectionModel
from app.models.section_members import SectionMembers
from app.models.template_course import TemplateCourse


def get_section_combined_data(db: Session, section_id: UUID, student_id: UUID):
    is_member = (
        db.query(SectionMembers)
        .filter(SectionMembers.section_id == section_id, SectionMembers.student_id == student_id)
        .first()
    )

    if not is_member:
        return None

    
    section = (
        db.query(SectionModel)
        .filter(SectionModel.section_id == section_id)
        .options(
            joinedload(SectionModel.announcements),
            joinedload(SectionModel.section_exclusive_contents),
            joinedload(SectionModel.template_course).joinedload(TemplateCourse.course_materials)
        )
        .first()
    )

    if not section:
        return None

    
    return section