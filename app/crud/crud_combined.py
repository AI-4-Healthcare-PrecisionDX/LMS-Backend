from uuid import UUID
from sqlalchemy.orm import Session
from app.models import Announcement, SectionExclusiveContent, Assignment

def get_section_combined_data(db: Session, section_id: UUID):
    announcements = db.query(Announcement).filter(Announcement.section_id == section_id).all()
    section_contents = db.query(SectionExclusiveContent).filter(SectionExclusiveContent.section_id == section_id).all()
    assignments = db.query(Assignment).filter(Assignment.section_id == section_id).all()

    return {
        "announcements": announcements,
        "section_exclusive_contents": section_contents,
        "assignments": assignments
    }
