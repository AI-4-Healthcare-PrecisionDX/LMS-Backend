from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.user_settings import UserSettings
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserCreateBySuperUser,
    UserCreateTeacher,
    UserCreateStudent,
    UserCreateAdmin,
    Student,
    Teacher,
)
from app.models.admin import Admin
from app.models.teacher import Teacher
from app.models.student import Student


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, *, id: str) -> Optional[User]:
        return db.query(User).filter(User.user_id == id).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        unique_username = (
            f"{obj_in.first_name.lower()}.{obj_in.last_name.lower()}.{uuid4().hex[:5]}"
        )
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            username=unique_username,
            gender=obj_in.gender,
            phone_number=obj_in.phone_number,
            role="user",
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        user_settings = UserSettings(user_id=db_obj.user_id)
        db.add(user_settings)
        db.commit()
        db.refresh(user_settings)

        return db_obj

    def create_admin_by_admin(
        self, db: Session, *, obj_in: UserCreateAdmin, branch_id: UUID
    ) -> User:
        unique_username = (
            f"{obj_in.first_name.lower()}_{obj_in.last_name.lower()}_{uuid4().hex[:5]}"
        )
        db_obj = self.create(db, obj_in=obj_in)
        db_obj.role = "admin"
        db_obj.branch_id = branch_id
        db.commit()
        db.refresh(db_obj)

        admin = Admin(user_id=db_obj.user_id)
        db.add(admin)
        db.commit()
        db.refresh(admin)

        result = db.query(User).filter(User.user_id == db_obj.user_id).first()
        return result

    def create_teacher_by_admin(
        self, db: Session, *, obj_in: UserCreateTeacher, branch_id: UUID
    ) -> User:
        unique_username = (
            f"{obj_in.first_name.lower()}_{obj_in.last_name.lower()}_{uuid4().hex[:5]}"
        )
        db_obj = self.create(db, obj_in=obj_in)
        db_obj.role = "teacher"
        db_obj.branch_id = branch_id
        db.commit()
        db.refresh(db_obj)

        teacher = Teacher(user_id=db_obj.user_id)
        db.add(teacher)
        db.commit()
        db.refresh(teacher)

        result = db.query(User).filter(User.user_id == db_obj.user_id).first()
        return result

    def create_student_by_admin(
        self, db: Session, *, obj_in: UserCreateStudent, branch_id: UUID
    ) -> User:
        unique_username = (
            f"{obj_in.first_name.lower()}_{obj_in.last_name.lower()}_{uuid4().hex[:5]}"
        )
        db_obj = self.create(db, obj_in=obj_in)
        db_obj.role = "student"
        db_obj.branch_id = branch_id
        db.commit()
        db.refresh(db_obj)

        student = Student(user_id=db_obj.user_id, metric_id=obj_in.metric_id)
        db.add(student)
        db.commit()
        db.refresh(student)

        result = db.query(User).filter(User.user_id == db_obj.user_id).first()
        return result

    def get_teacher_by_id(
        self, db: Session, *, id: UUID
    ) -> Optional[Teacher]:  # Changed parameter name from teacher_id to id
        return db.query(Teacher).filter(Teacher.teacher_id == id).first()

    def get_teacher_by_user_id(
        self, db: Session, *, id: UUID
    ) -> Optional[Teacher]:  # Changed parameter name from teacher_id to id
        return db.query(Teacher).filter(Teacher.user_id == id).first()

    def get_student_by_user_id(
        self, db: Session, *, id: UUID
    ) -> Optional[Student]:  # Keep consistent naming
        return db.query(Student).filter(Student.user_id == id).first()

    def get_student_by_id(
        self, db: Session, *, id: UUID
    ) -> Optional[Student]:  # Keep consistent naming

        return db.query(Student).filter(Student.student_id == id).first()

    def get_all_teachers(
        self, db: Session, *, skip: int = 0, limit: int = 100, branch_id: UUID
    ) -> list[User]:
        # Get those teachers from the database whose branch_id matches the branch_id passed as an argument.
        teachers = (
            db.query(User)
            .filter(User.branch_id == branch_id, User.role == "teacher")
            .offset(skip)
            .limit(limit)
            .all()
        )
        return teachers

    def get_all_students(
        self, db: Session, *, skip: int = 0, limit: int = 100, branch_id: UUID
    ) -> list[Student]:
        students = (
            db.query(User)
            .filter(User.branch_id == branch_id, User.role == "student")
            .offset(skip)
            .limit(limit)
            .all()
        )
        return students

    def create_student(self, db: Session, *, obj_in: UserCreateStudent) -> Student:
        unique_username = (
            f"{obj_in.first_name.lower()}.{obj_in.last_name.lower()}.{uuid4().hex[:5]}"
        )
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            username=unique_username,
            phone_number=obj_in.phone_number,
            gender=obj_in.gender,
            role="student",
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        student = Student(user_id=db_obj.user_id, metric_id=obj_in.metric_id)
        db.add(student)
        db.commit()
        db.refresh(student)

        user_settings = UserSettings(user_id=db_obj.user_id)
        db.add(user_settings)
        db.commit()
        db.refresh(user_settings)

        db_obj.metric_id = obj_in.metric_id

        return db_obj

    def create_superuser(
        self, db: Session, *, obj_in: UserCreateBySuperUser, username: str
    ) -> User:

        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            username=username,
            is_superuser=True,
            role="superuser",
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        user_settings = UserSettings(user_id=db_obj.user_id)
        db.add(user_settings)
        db.commit()
        db.refresh(user_settings)

        return db_obj

    def create_by_superuser(
        self, db: Session, *, obj_in: UserCreateBySuperUser, branch_id: str
    ) -> User:
        unique_username = (
            f"{obj_in.first_name.lower()}_{obj_in.last_name.lower()}_{uuid4().hex[:5]}"
        )
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            username=unique_username,
            role="admin",
            branch_id=branch_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        user_settings = UserSettings(user_id=db_obj.user_id)
        db.add(user_settings)
        db.commit()
        db.refresh(user_settings)

        return db_obj

    def create_admin(self, db: Session, *, user_id: str):
        db_obj = Admin(user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate | Dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data["password"]:
            password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
