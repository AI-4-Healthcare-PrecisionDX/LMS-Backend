from .user import User, UserCreate, UserInDB, UserUpdate, UserCreateBySuperUser
from .token import Token, TokenPayload
from .super_admin import (
    Department,
    DepartmentCreate,
    DepartmentUpdate,
    Branch,
    BranchCreate,
    https://github.com/AI-4-Healthcare-PrecisionDX/LMS-Backend/pull/25/conflict?name=app%252Fschemas%252F__init__.py&ancestor_oid=c86dff74efd5b72efff75291feb2468242c75b88&base_oid=bb7a83ac5ea1d576d8fc37427310a3ca90582125&head_oid=0d20baadba6c60b85647211c1a30f3f1f77db46bBranchUpdate,
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
    AssignmentOut,
    AssignmentQuestionBase,
    AssignmentQuestionCreate,
    AssignmentQuestionUpdate,
    AssignmentQuestionOut,
)

from .discussion import (
    Discussion,
    DiscussionCreate,
)

from .discussion_message import (
    DiscussionMessage,
    DiscussionMessageCreate,
    DiscussionMessageBase
)

from .discussion_reply_message import (
    DiscussionReplyMessage,
    DiscussionReplyMessageCreate,
    DiscussionReplyMessageBase
)

