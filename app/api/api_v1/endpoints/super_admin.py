from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session


from app import crud, models, schemas
from app.api import deps

router = APIRouter()


# Create a user as admin user
@router.post("/create-admin/{branch_id}", response_model=schemas.User)
def create_admin_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreateBySuperUser,
    branch_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> schemas.User:
    """
    Create a new user as admin for particular institution using institution branch id.
    """
    # Check if the user already exists
    try:
        user = crud.user.get_by_email(db, email=user_in.email)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the user",
        )

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )

    # Check if the branch exists
    try:
        branch = crud.branch.get_branch_by_id(db, id=branch_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the branch",
        )

    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")

    # Create a user
    try:
        user = crud.user.create_by_superuser(db, obj_in=user_in, branch_id=branch_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user",
        )

    # Create a Admin
    try:
        admin = crud.user.create_admin(db, user_id=user.user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the admin",
        )
    return user


# Create a new institution
@router.post("/create_institution", response_model=schemas.Institution)
def create_institution(
    *,
    db: Session = Depends(deps.get_db),
    institution_in: schemas.InstitutionCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a new institution (Only for Super Admin).
    """
    try:
        institution = crud.institution.create_institution(db, obj_in=institution_in)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the institution",
        )
    return institution


# Get the list of institutions
@router.get("/institutions", response_model=List[schemas.Institution])
def read_institutions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve institutions.
    """
    try:
        institutions = crud.institution.get_multi(db, skip=skip, limit=limit)
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the institutions",
        )
    return institutions


# Get an institution by ID
@router.get("/institutions/{institution_id}", response_model=schemas.Institution)
def read_institution_by_id(
    institution_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get a specific institution by ID.
    """
    try:
        institution = crud.institution.get_institution_by_id(db, id=institution_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the institution",
        )
    if institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")
    return institution


# Update an institution
@router.put("/institutions/{institution_id}", response_model=schemas.Institution)
def update_institution(
    *,
    db: Session = Depends(deps.get_db),
    institution_id: UUID,
    institution_in: schemas.InstitutionUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an institution.
    """
    try:
        institution = crud.institution.get_institution_by_id(db, id=institution_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the institution",
        )
    if institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")
    institution = crud.institution.update_institution(
        db, db_obj=institution, obj_in=institution_in
    )
    return institution


# Create a new branch
@router.post("/create_branch/{institution_id}", response_model=schemas.Branch)
def create_branch(
    *,
    db: Session = Depends(deps.get_db),
    branch_in: schemas.BranchCreate,
    institution_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new branch.
    """
    try:
        get_institution = crud.institution.get_institution_by_id(db, id=institution_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the institution",
        )

    if get_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    try:
        branch = crud.branch.create_branch(
            db, obj_in=branch_in, institution_id=institution_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the branch",
        )
    return branch


# Get the list of branches
@router.get("/branches", response_model=List[schemas.Branch])
def read_branches(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve branches.
    """
    try:
        branches = crud.branch.get_multi(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the branches",
        )
    return branches


# Get a branch by ID
@router.get("/branches/{branch_id}", response_model=schemas.Branch)
def read_branch_by_id(
    branch_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get a specific branch by ID.
    """
    try:
        branch = crud.branch.get_branch_by_id(db, id=branch_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the branch",
        )
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch


# Update a branch
@router.put("/branches/{branch_id}", response_model=schemas.Branch)
def update_branch(
    *,
    db: Session = Depends(deps.get_db),
    branch_id: str,
    branch_in: schemas.BranchUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a branch.
    """
    try:
        branch = crud.branch.get_branch_by_id(db, id=branch_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the branch",
        )
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    branch = crud.branch.update_branch(db, db_obj=branch, obj_in=branch_in)
    return branch


# Create a new department
@router.post("/create_department", response_model=schemas.Department)
def create_department(
    *,
    db: Session = Depends(deps.get_db),
    department_in: schemas.DepartmentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new department.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admins can perform this action"
        )
    
    try:
        department = crud.department.create_department(db, obj_in=department_in, branch_id=current_user.branch_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the department",
        )
    return department


# Get the list of departments
@router.get("/departments", response_model=List[schemas.Department])
def read_departments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve departments.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admins and superadmins can perform this action"
        )
        
    try:
        departments = crud.department.get_multi(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the departments",
        )
    return departments


# Get a department by ID
@router.get("/departments/{department_id}", response_model=schemas.Department)
def read_department_by_id(
    department_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific department by ID.
    """
    
    if current_user.role != "admin" and current_user.role != "superuser":
        raise HTTPException(
            status_code=403, detail="Only admins can perform this action"
        )
        
    try:
        department = crud.department.get_department_by_id(db, id=department_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the department",
        )
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


# Update a department
@router.put("/departments/{department_id}", response_model=schemas.Department)
def update_department(
    *,
    db: Session = Depends(deps.get_db),
    department_id: str,
    department_in: schemas.DepartmentUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a department.
    """
    
    if current_user.role != "admin" and current_user.role != "superuser":
        raise HTTPException(
            status_code=403, detail="Only admins can perform this action"
        )
        
        
    try:
        department = crud.department.get_department_by_id(db, id=department_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the department",
        )
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    department = crud.department.update_department(
        db, db_obj=department, obj_in=department_in
    )
    return department
