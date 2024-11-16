# app/schemas/__init__.py

from .user import (
    User,
    UserCreate,
    UserInDB,
    UserUpdate,
    UserCreateBySuperUser,
    Teacher,
    Admin,
    Student,
    UserCreateTeacher,
    UserCreateAdmin,
    UserCreateStudent,
)

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


from .section import (
    SectionBase,
    SectionCreate,
    SectionUpdate,
    SectionExclusiveContentBase,
    SectionExclusiveContentCreate,
    SectionExclusiveContentByCourseTeacher,
    SectionExclusiveContentByCourseTeacherCreate,
)

from .library import (
    Library,
    LibraryCreate,
    LibraryUpdate,
    LibraryInDBBase,
)



from .assignment import (
    AssignmentBase,
    AssignmentCreate,
    AssignmentUpdate,
    Assignment,
    AssignmentQuestionBase,
    AssignmentQuestionCreate,
    AssignmentQuestionUpdate,
    AssignmentQuestionInDB,
    AssignmentMaterialBase,
    AssignmentMaterialInDB,
    DeleteAssignmentResponse
)

from .discussion import (
    Discussion,
    DiscussionCreate,
)

from .discussion_message import (
    DiscussionMessage,
    DiscussionMessageCreate,
    DiscussionMessageBase,
)

from .discussion_reply_message import (
    DiscussionReplyMessage,
    DiscussionReplyMessageCreate,
    DiscussionReplyMessageBase,
)

