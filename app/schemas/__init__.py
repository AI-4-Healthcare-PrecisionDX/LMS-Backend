from .user import User, UserCreate, UserInDB, UserUpdate, UserCreateBySuperUser
from .token import Token, TokenPayload
from .super_admin import (
    Department,
    DepartmentCreate,
    DepartmentUpdate,
    Branch,
    BranchCreate,
    BranchUpdate,
    Institution,
    InstitutionCreate,
    InstitutionUpdate,
)

from .course import (
    TemplateCourse,
    TemplateCourseCreate,
    TemplateCourseUpdate,
)