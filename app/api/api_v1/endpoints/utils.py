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
import boto3
from botocore.exceptions import ClientError
import uuid
from PyPDF2 import PdfReader
from io import BytesIO
from datetime import datetime, timedelta


from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.post("/library/file_upload", response_model=schemas.Library)
def upload_file(
    db: Session = Depends(deps.get_db),
    pdf_file: UploadFile = File(...),  # Required
    json_file: Optional[UploadFile] = File(default=None),  # Optional
    material_type: str = Form(...),
    material_title: str = Form(...),
    material_description: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    visibility: Optional[bool] = Form(True),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    # Validate JSON file type only if it's provided
    if json_file and json_file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="JSON file must be of type application/json")

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        folder_name = str(uuid.uuid4())[:16]
        
        # Upload PDF file
        pdf_file.file.seek(0)
        s3_client.put_object(
            Bucket=settings.AWS_S3_BUCKET,
            Key=f"{folder_name}/{pdf_file.filename}",
            Body=pdf_file.file,
            ContentType=pdf_file.content_type
        )

        # Upload JSON file if provided
        if json_file:
            json_file.file.seek(0)
            s3_client.put_object(
                Bucket=settings.AWS_S3_BUCKET,
                Key=f"{folder_name}/{json_file.filename}",
                Body=json_file.file,
                ContentType=json_file.content_type
            )

    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while uploading. Please try again.",
        )

    if current_user.role == "admin":
        visibility = True
        
        
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
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        folder_name = library.material_file
        
        # List objects in the folder
        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_S3_BUCKET,
            Prefix=f"{folder_name}/"
        )
        
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith(".json"):
                    json_obj = s3_client.get_object(
                        Bucket=settings.AWS_S3_BUCKET,
                        Key=obj['Key']
                    )
                    json_data = json.loads(json_obj['Body'].read().decode("utf-8"))
                    break
    except ClientError as e:
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
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        folder_name = library.material_file
        
        # List objects in the folder
        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_S3_BUCKET,
            Prefix=f"{folder_name}/"
        )
        
        pdf_key = None
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith(".pdf"):
                    pdf_key = obj['Key']
                    break

        if not pdf_key:
            raise HTTPException(status_code=404, detail="PDF file not found")

        # Generate a signed URL that expires in 10 minutes
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_S3_BUCKET, 'Key': pdf_key},
            ExpiresIn=600  # 10 minutes in seconds
        )

        return {"file_url": url}

    except ClientError as e:
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
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        folder_name = library.material_file
        
        # List objects in the folder
        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_S3_BUCKET,
            Prefix=f"{folder_name}/"
        )
        
        pdf_key = None
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith(".pdf"):
                    pdf_key = obj['Key']
                    break

        if not pdf_key:
            raise HTTPException(status_code=404, detail="PDF file not found")

        # Generate a signed URL that expires in 10 minutes
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_S3_BUCKET, 'Key': pdf_key},
            ExpiresIn=600  # 10 minutes in seconds
        )

        return {"file_url": url,
                "material_type": library.material_type,
                "material_title": library.material_title,
                "material_description": library.material_description,
                "created_at": library.created_at,
                "updated_at": library.updated_at,
                "author": library.author,
                }

    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating file URL: {str(e)}",
        )


@router.delete("/library/{library_id}")
def delete_library(
    library_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    # current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Delete a library item from both database and AWS S3 storage.
    Only the owner of the library or an admin can delete it.
    """
    # Get the library item first to check permissions and get file info
    library = crud.library.get_by_uuid(db, library_id=library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    
    # Check permissions - only the owner or admin can delete
    # if library.user_id != current_user.user_id and current_user.role != "admin":
    #     raise HTTPException(
    #         status_code=403, 
    #         detail="You do not have permission to delete this library item"
    #     )

    try:
        # Delete files from S3 first
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        folder_name = library.material_file
        
        # List all objects in the folder
        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_S3_BUCKET,
            Prefix=f"{folder_name}/"
        )
        
        # Delete all objects in the folder
        if 'Contents' in response:
            objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
            s3_client.delete_objects(
                Bucket=settings.AWS_S3_BUCKET,
                Delete={'Objects': objects_to_delete}
            )

        # Delete from database (this will cascade delete related records)
        deleted_library = crud.library.delete_library(db=db, library_id=library_id)
        
        return {
            "message": "Library item and associated files deleted successfully",
            "deleted_library": {
                "library_id": str(deleted_library.library_id),
                "material_title": deleted_library.material_title,
                "material_type": deleted_library.material_type
            }
        }

    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting files from S3: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the library item: {str(e)}"
        )
