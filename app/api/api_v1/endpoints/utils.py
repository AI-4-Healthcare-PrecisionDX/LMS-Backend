from typing import Any, List, Optional
import json
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    UploadFile,
    File,
    BackgroundTasks,
    Form,
)
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from google.cloud import storage
import uuid
from PyPDF2 import PdfReader
from io import BytesIO
from datetime import datetime, timedelta


from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.post("library/file_upload", response_model=schemas.Library)
def upload_file(
    db: Session = Depends(deps.get_db),
    pdf_file: UploadFile = File(...),
    json_file: UploadFile = File(...),
    material_type: str = Form(...),
    material_title: str = Form(...),
    material_description: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    visibility: Optional[bool] = Form(True),
    current_user: models.User = Depends(deps.get_current_active_user),
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

    library_in = schemas.LibraryCreate(
        material_type=material_type,
        material_title=material_title,
        material_description=material_description,
        author=author,
        visibility=visibility,
    )

    try:
        library = crud.library.create_by_user(
            db=db,
            obj_in=library_in,
            user_id=current_user.user_id,
            material_file=folder_name,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while saving to database. Please try again.",
        )

    return library


# Get all public libraries also user for the current user
@router.get("/libraries", response_model=List[schemas.Library])
def read_libraries(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    try:
        libraries = crud.library.get_all_public_and_user_created(
            db=db, user_id=current_user.user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching data."
        )

    return libraries


# Get a library by its UUID where the user is the owner of the library or the library is public
@router.get("/library/{library_id}")
def read_library_by_uuid(
    library_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    library = crud.library.get_by_uuid(db, library_id=library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    if library.user_id != current_user.user_id and not library.visibility:
        raise HTTPException(
            status_code=403, detail="You do not have permission to access this library"
        )
    json_data = None
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.GOOGLE_STORAGE_BUCKET)
        folder_name = library.material_file
        blobs = bucket.list_blobs(prefix=f"{folder_name}/")
        for blob in blobs:
            if blob.name.endswith(".json"):
                json_blob = blob.download_as_bytes()
                json_data = json.loads(json_blob.decode("utf-8"))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching files."
        )

    return {
        "content_meta": library,
        "content_outline": json_data,
    }


@router.get("/library/{library_id}/file")
def get_library_file_url(
    library_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    library = crud.library.get_by_uuid(db, library_id=library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    if library.user_id != current_user.user_id and not library.visibility:
        raise HTTPException(
            status_code=403, detail="You do not have permission to access this library"
        )

    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.GOOGLE_STORAGE_BUCKET)
        folder_name = library.material_file
        blobs = bucket.list_blobs(prefix=f"{folder_name}/")
        pdf_blob = next((blob for blob in blobs if blob.name.endswith(".pdf")), None)

        if not pdf_blob:
            raise HTTPException(status_code=404, detail="PDF file not found")

        # Generate a signed URL that expires in 1 hour
        url = pdf_blob.generate_signed_url(
            version="v4",
            expiration=datetime.utcnow() + timedelta(minutes=10),
            method="GET",
        )

        return {"file_url": url}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating file URL: {str(e)}",
        )



@router.get("/library_course_section/file/{library_id}")
def get_library_file_url_for_course_and_section_contents(
    library_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    library = crud.library.get_by_uuid(db, library_id=library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    # if library.user_id != current_user.user_id and not library.visibility:
    #     raise HTTPException(
    #         status_code=403, detail="You do not have permission to access this library"
    #     )

    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.GOOGLE_STORAGE_BUCKET)
        folder_name = library.material_file
        blobs = bucket.list_blobs(prefix=f"{folder_name}/")
        pdf_blob = next((blob for blob in blobs if blob.name.endswith(".pdf")), None)

        if not pdf_blob:
            raise HTTPException(status_code=404, detail="PDF file not found")

        # Generate a signed URL that expires in 1 hour
        url = pdf_blob.generate_signed_url(
            version="v4",
            expiration=datetime.utcnow() + timedelta(minutes=10),
            method="GET",
        )

        return {"file_url": url,
                "material_type": library.material_type,
                "material_title": library.material_title,
                "material_description": library.material_description,
                "created_at": library.created_at,
                "updated_at": library.updated_at,
                "author": library.author,
                }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating file URL: {str(e)}",
        )
