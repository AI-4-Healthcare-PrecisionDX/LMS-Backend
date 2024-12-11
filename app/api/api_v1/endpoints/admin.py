# app/api/api_v1/endpoints/admin.py

from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from uuid import UUID

router = APIRouter()


# Admin can create a new user.
# Assign the role of the user to be (admin, teacher, student).
# Admin can create a new library, template_course.


# Create admin user
@router.post("/create-admin", response_model=schemas.Admin)
def create_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreateAdmin,
    # branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> schemas.Admin:
    """
    Create a new admin for a specific branch.
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

    try:
        user = crud.user.create_admin_by_admin(
            db, obj_in=user_in, branch_id=current_user.branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user",
        )
    return user


@router.get("/admins", response_model=List[schemas.Admin])
def get_admins(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve all admins of a particular branch.
    """
    try:
        admins = crud.user.get_all_admins(
            db, skip=skip, limit=limit, branch_id=current_user.branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the admins",
        )
    return admins


@router.put("/update-admin", response_model=schemas.Admin)
def update_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> schemas.Admin:
    """
    Update an admin.
    """
    try:
        user = crud.user.get_by_email(db, email=user_in.email)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the user",
        )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        user = crud.user.update(db, db_obj=user, obj_in=user_in)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while updating the user",
        )
    return user


# Create teacher user
@router.post("/create-teacher", response_model=schemas.Teacher)
def create_teacher(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreateTeacher,
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> schemas.Teacher:
    """
    Create a new teacher for a specific branch.
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
    try:
        user = crud.user.create_teacher_by_admin(
            db, obj_in=user_in, branch_id=current_user.branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user",
        )
    return user


@router.get("/teachers", response_model=List[schemas.Teacher])
def get_teachers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve all teachers of a particular branch.
    """
    try:
        teachers = crud.user.get_all_teachers(
            db, skip=skip, limit=limit, branch_id=current_user.branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the teachers",
        )
    return teachers


@router.get(
    "/teachers/{branch_id}/teacher/{teacher_id}",
    response_model=schemas.user.UserInDBTeacher,
)
def get_teacher_by_id(
    teacher_id: UUID,
    db: Session = Depends(deps.get_db),
    branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve teacher by id.
    """
    try:
        teacher = crud.user.get_teacher_by_id(db, id=teacher_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the teacher",
        )
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher



@router.put("/update-teacher", response_model=schemas.Teacher)
def update_teacher(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> schemas.Teacher:
    """
    Update a teacher.
    """
    try:
        user = crud.user.get_by_email(db, email=user_in.email)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the user",
        )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        user = crud.user.update(db, db_obj=user, obj_in=user_in)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while updating the user",
        )
    return user


#delete teacher
@router.delete("/delete-teacher/{teacher_id}")
def delete_teacher(
    teacher_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> dict:
    """
    Delete a teacher.
    """
    try:
        teacher = crud.user.get_teacher_by_id(db, id=teacher_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the teacher",
        )
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    crud.user.delete_user(db, user_id=teacher.user_id)
    return {"detail": "Teacher deleted successfully"}


@router.post("/create-student", response_model=schemas.Student)
def create_student(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreateStudent,
    # branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> schemas.Student:
    """
    Create a new student for a specific branch.
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

    try:
        user = crud.user.create_student_by_admin(
            db, obj_in=user_in, branch_id=current_user.branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user",
        )
    return user


@router.get("/students", response_model=List[schemas.Student])
def get_students(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve all students of a particular branch.
    """
    try:
        students = crud.user.get_all_students(
            db, skip=skip, limit=limit, branch_id=current_user.branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the students",
        )
    return students


@router.get(
    "/students/{branch_id}/student/{student_id}", response_model=schemas.Student
)
def get_student_by_id(
    student_id: UUID,
    db: Session = Depends(deps.get_db),
    branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve student by id.
    """
    try:
        student = crud.user.get_student_by_id(db, id=student_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the student",
        )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/update-student", response_model=schemas.Student)
def update_student(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> schemas.Student:
    """
    Update a student.
    """
    try:
        user = crud.user.get_by_email(db, email=user_in.email)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the user",
        )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        user = crud.user.update(db, db_obj=user, obj_in=user_in)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while updating the user",
        )
    return user


#delete student
@router.delete("/delete-student/{student_id}")
def delete_student(
    student_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> dict:
    """
    Delete a student.
    """
    try:
        student = crud.user.get_student_by_id(db, id=student_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the student",
        )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    try:
        crud.user.delete_user(db, user_id=student.user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the student",
        )
        
    return {"detail": "Student deleted successfully"}



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
        department = crud.department.create_department(
            db, obj_in=department_in, branch_id=current_user.branch_id
        )
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
            status_code=403, detail="Only admins can perform this action"
        )

    try:
        departments = crud.department.get_departments_by_branch(
            db, branch_id=current_user.branch_id
        )
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

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admins can perform this action"
        )

    try:
        department = crud.department.get_department_by_id(
            db, department_id=department_id, branch_id=current_user.branch_id
        )
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
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a department.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admins can perform this action"
        )

    try:
        department = crud.department.get_department_by_id(
            db, department_id=department_id, branch_id=current_user.branch_id
        )
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


#delete department
@router.delete("/delete-department/{department_id}")
def delete_department(
    department_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> dict:
    """
    Delete a department.
    """

    try:
        department = crud.department.get_department_by_id(
            db, department_id=department_id, branch_id=current_user.branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the department",
        )
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    
    try:
        crud.department.delete_department(db, department_id=department_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the department",
        )
        
    return {"detail": "Department deleted successfully"}



@router.post("/create_scenario")
def create_scenario(
    scenario_in: schemas.scenario.ScenarioData,
    db=Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admins can perform this action"
        )

    # Get the scenario from scene_in
    scenario = scenario_in.scenario
    # Get the scenario_examination_findings from scene_in
    scenario_examination_findings = scenario_in.scenario_examination_findings

    # Create the scenario
    scenario = crud.crud_scenario.scenario.create_scenario(
        db=db,
        obj_in=scenario,
        department_id=scenario_in.department_id,
        branch_id=current_user.branch_id,
    )

    # Create the scenario_examination_findings
    try:
        scenario_examination_findings = crud.crud_scenario.scenario_examination_finding.create_scenario_examination_findings(
            db=db,
            obj_in=scenario_examination_findings,
            scenario_id=scenario.scenario_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the scenario examination findings",
        )

    return {"detail": "Scenario created successfully"}


# Get all scenarios
@router.get(
    "/scenarios", response_model=List[schemas.scenario.ScenarioWithExaminationFinding]
)
def get_all_scenarios(
    db=Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_user),
):
    try:
        scenarios = crud.crud_scenario.scenario.get_scenario_with_findings(
            db=db, branch_id=current_user.branch_id
        )
        return [
            schemas.scenario.ScenarioWithExaminationFinding(
                scenario=scenario.__dict__,
                scenario_examination_findings=scenario.scenario_examination_findings.__dict__,
            )
            for scenario in scenarios
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the scenarios",
        )


