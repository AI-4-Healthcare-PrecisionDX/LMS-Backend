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


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    if user_in.email is not None and user_in.email != current_user.email:
        raise HTTPException(
            status_code=400,
            detail="Users are not allowed to change their email address.",
        )

    try:
        updated_user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return updated_user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/files")
def read_files():
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.GOOGLE_STORAGE_BUCKET)
        # 0012708b-40dc-41 is the folder name
        blobs = bucket.list_blobs(prefix="0012708b-40dc-41")
        json_data = None
        pdf_blob = None
        for blob in blobs:
            if blob.name.endswith(".json"):
                json_blob = blob.download_as_bytes()
                json_data = json.loads(json_blob.decode("utf-8"))
            if blob.name.endswith(".pdf"):
                pdf_blob = blob.download_as_bytes()

        if json_data is None:
            raise HTTPException(status_code=404, detail="JSON file not found")
        if pdf_blob is None:
            raise HTTPException(status_code=404, detail="PDF file not found")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while parsing JSON file"
        )
    except Exception as e:
        print(f"Error fetching files: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching files"
        )

    try:
        pdf_file = BytesIO(pdf_blob)
        pdf_reader = PdfReader(pdf_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while reading PDF file"
        )

    return {"content": json_data, "pdf": pdf_text}


# File upload
@router.post("/upload")
def upload_file(
    pdf_file: UploadFile = File(...),
    json_file: UploadFile = File(...),
):
    if (
        pdf_file.content_type != "application/pdf"
        or json_file.content_type != "application/json"
    ):
        raise HTTPException(status_code=400, detail="Only PDF and JSON files allowed")

    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.GOOGLE_STORAGE_BUCKET)
        # create a folder in the bucket with a unique name using uuid upto 16 characters
        folder_name = str(uuid.uuid4())[:16]
        folder = bucket.blob(folder_name)
        # upload the files to the folder
        pdf_blob = bucket.blob(f"{folder_name}/{pdf_file.filename}")
        pdf_blob.upload_from_file(pdf_file.file)
        json_blob = bucket.blob(f"{folder_name}/{json_file.filename}")
        json_blob.upload_from_file(json_file.file)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while uploading. Please try again.",
        )

    return f"Files uploaded successfully to {folder_name}"


# @router.post("/open", response_model=schemas.User)
# def create_user_open(
#     *,
#     db: Session = Depends(deps.get_db),
#     password: str = Body(...),
#     email: EmailStr = Body(...),
#     full_name: str = Body(None),
# ) -> Any:
#     """
#     Create new user without the need to be logged in.
#     """
#     if not settings.USERS_OPEN_REGISTRATION:
#         raise HTTPException(
#             status_code=403,
#             detail="Open user registration is forbidden on this server",
#         )
#     user = crud.user.get_by_email(db, email=email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system",
#         )
#     user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
#     user = crud.user.create(db, obj_in=user_in)
#     return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
