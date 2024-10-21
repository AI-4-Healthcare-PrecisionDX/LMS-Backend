from fastapi import APIRouter


from app.api.api_v1.endpoints import login, users, super_admin, admin, course, utils,section


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(
    super_admin.router, prefix="/super_admin", tags=["super_admin"]
)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(course.router, prefix="/course", tags=["course"])

api_router.include_router(section.router, prefix="/section",tags=["section"])

api_router.include_router(utils.router, prefix="/utils", tags=["utils"])

# api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
# api_router.include_router(student.router, prefix="/student", tags=["student"])
