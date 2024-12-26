from sqlmodel import SQLModel, Field
from datetime import datetime


class Employee(SQLModel, table=True):
    """
    Represents an employee in the organization.

    This model captures comprehensive information about an employee,
    including personal details, job assignment, and hiring information.

    Attributes
    ----------
    id : int
        Unique identifier for the employee.
        Serves as the primary key in the database.

    name : str
        Full name of the employee.

    hire_datetime : datetime
        Date and time when the employee was hired.
        Can be None if hiring date is not specified.

    department_id : int
        Identifier of the department the employee belongs to.
        References the Department model's primary key.
        Can be None if department is not assigned.

    job_id : int
        Identifier of the job position of the employee.
        References the Job model's primary key.
        Can be None if job position is not assigned.

    Examples
    --------
    >>> from datetime import datetime
    >>> emp = Employee(
    ...     id=1,
    ...     name="John Doe",
    ...     hire_datetime=datetime.now(),
    ...     department_id=1,
    ...     job_id=2
    ... )
    >>> emp.name
    'John Doe'
    """
    __tablename__ = "employees"

    id: int = Field(primary_key=True)
    name: str
    hire_datetime: datetime
    department_id: int = Field(foreign_key="departments.id")
    job_id: int = Field(foreign_key="jobs.id")
