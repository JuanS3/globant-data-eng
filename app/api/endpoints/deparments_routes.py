from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlmodel import Session
import pandas as pd
import io

from core.database import get_session
from models.department import Department
from services.department_service import DepartmentService
from core.exceptions import ResourceNotFoundError, DatabaseOperationError


router = APIRouter(prefix='/departments', tags=['departments'])


@router.post('/', response_model=Department)
def create_department(department: Department, session: Session = Depends(get_session)):
    """
    Create a new department.

    Parameters
    ----------
    department : Department
        Department details to be created
    session : Session
        Database session dependency

    Returns
    -------
    Department
        Created department with assigned ID
    """
    try:
        department_service = DepartmentService(session)
        return department_service.create(department)
    except DatabaseOperationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{department_id}', response_model=Department)
def get_department(department_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a department by its ID.

    Parameters
    ----------
    department_id : int
        Unique identifier of the department
    session : Session
        Database session dependency

    Returns
    -------
    Department
        Department details
    """
    try:
        department_service = DepartmentService(session)
        return department_service.get_by_id(department_id)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/', response_model=list[Department])
def list_departments(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    List all departments with optional pagination.

    Parameters
    ----------
    offset : int, optional
        Number of records to skip, by default 0
    limit : int, optional
        Maximum number of records to return, by default 100
    session : Session
        Database session dependency

    Returns
    -------
    list[Department]
        List of departments
    """
    department_service = DepartmentService(session)
    return department_service.get_all(offset, limit)


@router.put('/{department_id}', response_model=Department)
def update_department(
    department_id: int,
    department_update: Department,
    session: Session = Depends(get_session),
):
    """
    Update an existing department.

    Parameters
    ----------
    department_id : int
        Unique identifier of the department to update
    department_update : Department
        Updated department details
    session : Session
        Database session dependency

    Returns
    -------
    Department
        Updated department details
    """
    try:
        department_service = DepartmentService(session)
        return department_service.update(department_id, department_update)
    except (ResourceNotFoundError, DatabaseOperationError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{department_id}', status_code=204)
def delete_department(department_id: int, session: Session = Depends(get_session)):
    """
    Delete a department by its ID.

    Parameters
    ----------
    department_id : int
        Unique identifier of the department to delete
    session : Session
        Database session dependency
    """
    try:
        department_service = DepartmentService(session)
        department_service.delete(department_id)
    except (ResourceNotFoundError, DatabaseOperationError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/csv/')
async def upload_department_csv(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
) -> dict[str, str]:
    """
    Upload a CSV file containing department data.

    Parameters:
    -----------
    file : UploadFile
        The CSV file to be uploaded
    session : Session
        Database session dependency

    Returns:
    --------
    dict
        A dictionary with upload status and details
    """
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), names=['id', 'department'])
        department_service = DepartmentService(session)
        successful_imports = 0
        failed_imports = 0

        for _, row in df.iterrows():
            try:
                department = Department(id=row['id'], department=row['department'])
                department_service.create(department)
                successful_imports += 1
            except Exception:
                failed_imports += 1

        session.commit()

        return {
            'status': 'success',
            'successful_imports': str(successful_imports),
            'failed_imports': str(failed_imports),
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))