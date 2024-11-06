import datetime
from typing import Any, List
import json
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    UploadFile,
    File,
    BackgroundTasks,
)
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from google.cloud import storage
import uuid
from PyPDF2 import PdfReader
from io import BytesIO


from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
