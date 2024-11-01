#app/api/api_v1/endpoints/__init__.py

from .users import router as users_router
from .super_admin import router as super_admin_router
from .admin import router as admin_router
from .course import router as course_router
from .section import router as section_router

from .discussion_message import router as discussion_message_router
from .assignment import router as assignment_router

