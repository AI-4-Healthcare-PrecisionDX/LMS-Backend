from typing import Generator
from uuid import UUID
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.db.session import SessionLocal
from app.core.config import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get_by_id(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_admin_user(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> models.user.User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admins can perform this action"
        )

    admin = crud.user.get_admin_by_user_id(db, user_id=current_user.user_id)

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found",
        )

    return current_user


def get_current_active_teacher_user(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> models.Teacher:
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403, detail="Only teachers can perform this action"
        )

    teacher = crud.user.get_teacher_by_user_id(db, id=current_user.user_id)

    return teacher


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def check_branch(
    branch_id: UUID = Path(...),
    db: Session = Depends(get_db),
) -> UUID:
    """
    Verify if branch exists and return branch_id if valid.
    """
    branch = crud.branch.get_branch_by_id(db, id=branch_id)

    if not branch:
        raise HTTPException(
            status_code=404,
            detail=f"Branch not found",
        )

    return branch_id
