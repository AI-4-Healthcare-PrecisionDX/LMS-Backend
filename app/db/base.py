# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.user_settings import UserSettings  # noqa
from app.models.teacher import Teacher  # noqa
from app.models.admin import Admin  # noqa
from app.models.student import Student  # noqa
from app.models.branch import Branch  # noqa
from app.models.department import Department  # noqa
from app.models.institution import Institution  # noqa
from app.models.student_event import StudentEvent #noqa
