from sqlmodel import Session, select, col

from models.employee import Employee
from core.exceptions import DatabaseOperationError, ResourceNotFoundError


class EmployeeService:
    """
    Service class for managing Employee-related database operations.

    This service provides methods for CRUD (Create, Read, Update, Delete)
    operations on Employee entities with robust error handling and type safety.

    Attributes
    ----------
    session : Session
        SQLModel database session for performing database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize EmployeeService with a database session.

        Parameters
        ----------
        session : Session
            SQLModel database session for performing database operations.
        """
        self.session = session

    def create(self, employee: Employee) -> Employee:
        """
        Create a new employee in the database.

        Parameters
        ----------
        employee : Employee
            The employee entity to be created.

        Returns
        -------
        Employee
            The created employee with assigned database ID.

        Raises
        ------
        DatabaseOperationError
            If there's an error during employee creation.
        """
        try:
            self.session.add(employee)
            self.session.commit()
            self.session.refresh(employee)
            return employee
        except Exception as e:
            self.session.rollback()
            raise DatabaseOperationError(f"Error creating employee: {str(e)}") from e

    def get_by_id(self, employee_id: int) -> Employee:
        """
        Retrieve an employee by their unique identifier.

        Parameters
        ----------
        employee_id : int
            The unique identifier of the employee.

        Returns
        -------
        Employee
            The employee with the specified ID.

        Raises
        ------
        ResourceNotFoundError
            If no employee is found with the given ID.
        """
        employee = self.session.get(Employee, employee_id)
        if not employee:
            raise ResourceNotFoundError(f'Employee with ID {employee_id} not found')
        return employee

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Employee]:
        """
        Retrieve a list of employees with optional pagination.

        Parameters
        ----------
        offset : int, optional
            Number of records to skip, by default 0
        limit : int, optional
            Maximum number of records to return, by default 100

        Returns
        -------
        List[Employee]
            A list of employee entities.
        """
        statement = select(Employee).offset(offset).limit(limit)
        results = self.session.exec(statement)
        return list(results.all())

    def update(self, employee_id: int, employee_update: Employee) -> Employee:
        """
        Update an existing employee.

        Parameters
        ----------
        employee_id : int
            The unique identifier of the employee to update.
        employee_update : Employee
            The updated employee data.

        Returns
        -------
        Employee
            The updated employee entity.

        Raises
        ------
        ResourceNotFoundError
            If no employee is found with the given ID.
        DatabaseOperationError
            If there's an error during employee update.
        """
        existing_employee = self.get_by_id(employee_id)

        if not existing_employee:
            return None

        try:
            for key, value in employee_update.model_dump(exclude_unset=True).items():
                setattr(existing_employee, key, value)

            self.session.add(existing_employee)
            self.session.commit()
            self.session.refresh(existing_employee)
            return existing_employee
        except Exception as e:
            self.session.rollback()
            raise DatabaseOperationError(f'Error updating employee: {str(e)}') from e

    def delete(self, employee_id: int) -> None:
        """
        Delete an employee by their unique identifier.

        Parameters
        ----------
        employee_id : int
            The unique identifier of the employee to delete.

        Raises
        ------
        ResourceNotFoundError
            If no employee is found with the given ID.
        DatabaseOperationError
            If there's an error during employee deletion.
        """
        try:
            employee = self.get_by_id(employee_id)
            self.session.delete(employee)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise DatabaseOperationError(f'Error deleting employee: {str(e)}') from e

    def get_hired_by_quarter(self, year: int) -> list[dict]:
        """
        Get the number of employees hired per department and job in each quarter.

        Parameters
        ----------
        year : int
            The year to retrieve hiring data for.

        Returns
        -------
        List[dict]
            A list of dictionaries containing hiring statistics.
        """
        try:
            statement = (
                select(
                    Employee.department_id,
                    Employee.job_id,
                    (col(Employee.hire_datetime).quarter()).label("quarter"),
                    col(Employee.id).count().label("hired_count"),
                )
                .where(col(Employee.hire_datetime).year() == year)
                .group_by(Employee.department_id, Employee.job_id, "quarter")
                .order_by(Employee.department_id, Employee.job_id, "quarter")
            )

            results = self.session.exec(statement)
            return [dict(row) for row in results.all()]
        except Exception as e:
            raise DatabaseOperationError(
                f'Error retrieving hiring statistics: {str(e)}'
            ) from e
