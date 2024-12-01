# app/api/api_v1/api.py

from fastapi import APIRouter


from app.api.api_v1.endpoints import (
    announcement,
    login,
    users,
    super_admin,
    admin,
    course,
    utils,
    section,
    discussion,
    assignment,
    discussion_message,
    llm,
    notes,
    student_event,
    student
)


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(
    super_admin.router, prefix="/super_admin", tags=["super_admin"]
)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(course.router, prefix="/course", tags=["course"])

api_router.include_router(section.router, prefix="/section", tags=["section"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(assignment.router, prefix="/assignment", tags=["assignment"])

api_router.include_router(discussion.router, prefix="/discussion", tags=["discussion"])
api_router.include_router(
    discussion_message.router, prefix="/discussion_message", tags=["discussion_message"]
)

# api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
# api_router.include_router(student.router, prefix="/student", tags=["student"])


api_router.include_router(student_event.router, prefix="/student-event", tags=["student-event"])

api_router.include_router(llm.router, prefix="/llm", tags=["llm"])


api_router.include_router(notes.router, prefix="/notes", tags=["notes"])

api_router.include_router(announcement.router, prefix="/announcement", tags=["announcement"])

api_router.include_router(student.router, prefix="/student", tags=["student"])