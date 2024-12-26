from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlmodel import Session
import pandas as pd
import io

from core.database import get_session
from models.employee import Employee
from services.employee_service import EmployeeService
from core.exceptions import ResourceNotFoundError, DatabaseOperationError

router = APIRouter(prefix='/employees', tags=['employees'])


@router.post('/', response_model=Employee)
def create_employee(employee: Employee, session: Session = Depends(get_session)):
    """
    Create a new employee.

    Parameters
    ----------
    employee : Employee
        Employee details to be created
    session : Session
        Database session dependency

    Returns
    -------
    Employee
        Created employee with assigned ID
    """
    try:
        employee_service = EmployeeService(session)
        return employee_service.create(employee)
    except DatabaseOperationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{employee_id}', response_model=Employee)
def get_employee(employee_id: int, session: Session = Depends(get_session)):
    """
    Retrieve an employee by their ID.

    Parameters
    ----------
    employee_id : int
        Unique identifier of the employee
    session : Session
        Database session dependency

    Returns
    -------
    Employee
        Employee details
    """
    try:
        employee_service = EmployeeService(session)
        return employee_service.get_by_id(employee_id)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/', response_model=list[Employee])
def list_employees(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    List all employees with optional pagination.

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
    list[Employee]
        List of employees
    """
    employee_service = EmployeeService(session)
    return employee_service.get_all(offset, limit)


@router.put('/{employee_id}', response_model=Employee)
def update_employee(
    employee_id: int, employee_update: Employee, session: Session = Depends(get_session)
):
    """
    Update an existing employee.

    Parameters
    ----------
    employee_id : int
        Unique identifier of the employee to update
    employee_update : Employee
        Updated employee details
    session : Session
        Database session dependency

    Returns
    -------
    Employee
        Updated employee details
    """
    try:
        employee_service = EmployeeService(session)
        return employee_service.update(employee_id, employee_update)
    except (ResourceNotFoundError, DatabaseOperationError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{employee_id}', status_code=204)
def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    """
    Delete an employee by their ID.

    Parameters
    ----------
    employee_id : int
        Unique identifier of the employee to delete
    session : Session
        Database session dependency
    """
    try:
        employee_service = EmployeeService(session)
        employee_service.delete(employee_id)
    except (ResourceNotFoundError, DatabaseOperationError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/reports/hires/departments/q/{year}')
def get_hired_by_quarter(year: int, session: Session = Depends(get_session)):
    """
    Get the number of employees hired per department and job in each quarter.

    Parameters
    ----------
    year : int
        The year to retrieve hiring data for
    session : Session
        Database session dependency

    Returns
    -------
    list[dict]
        List of hiring statistics per department, job, and quarter
    """
    try:
        employee_service = EmployeeService(session)
        return employee_service.get_hired_by_quarter(year)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/csv/')
async def upload_employee_csv(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
) -> dict[str, str]:
    """
    Upload a CSV file containing employee data.

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
        df = pd.read_csv(
            io.BytesIO(contents),
            names=['id', 'name', 'datetime', 'department_id', 'job_id']
        )

        employee_service = EmployeeService(session)

        successful_imports = 0
        failed_imports = 0

        for _, row in df.iterrows():
            try:
                employee = Employee(
                    id=row['id'],
                    name=row['name'],
                    datetime=row['datetime'],
                    department_id=row['department_id'],
                    job_id=row['job_id'],
                )
                employee_service.create(employee)
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