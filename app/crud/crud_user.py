from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.user_settings import UserSettings
from app.schemas.user import UserCreate, UserUpdate, UserCreateBySuperUser,UserCreateTeacher,UserCreateStudent, UserInDBStudent, UserInDBTeacher
from app.models.admin import Admin
from app.models.teacher import Teacher
from app.models.student import Student
import uuid


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, *, id: str) -> Optional[User]:
        return db.query(User).filter(User.user_id == id).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        unique_username = f"{obj_in.first_name.lower()}.{obj_in.last_name.lower()}.{uuid.uuid4().hex[:8]}"
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            username=unique_username,
            gender=obj_in.gender,
            phone_number=obj_in.phone_number,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        user_settings = UserSettings(user_id=db_obj.user_id)
        db.add(user_settings)
        db.commit()
        db.refresh(user_settings)

        return db_obj
    
    
    def create_teacher(self, db: Session, *, obj_in: UserCreateTeacher) -> UserInDBTeacher:
        unique_username = f"{obj_in.first_name.lower()}.{obj_in.last_name.lower()}.{uuid.uuid4().hex[:8]}"
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            username=unique_username,
            phone_number=obj_in.phone_number,
            gender=obj_in.gender,
            role="teacher",
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        teacher = Teacher(user_id=db_obj.user_id)
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
        
        user_settings = UserSettings(user_id=db_obj.user_id)
        db.add(user_settings)
        db.commit()
        db.refresh(user_settings)
        
        return db_obj

    def create_student(self, db: Session, *, obj_in: UserCreateStudent) -> UserInDBStudent:
        unique_username = f"{obj_in.first_name.lower()}.{obj_in.last_name.lower()}.{uuid.uuid4().hex[:8]}"
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
        self, db: Session, *, obj_in: UserCreateBySuperUser
    ) -> User:
        unique_username = f"{obj_in.first_name.lower()}.{obj_in.last_name.lower()}.{uuid.uuid4().hex[:8]}"
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            username=unique_username,
            role="admin",
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
