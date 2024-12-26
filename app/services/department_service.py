from sqlmodel import Session, select

from models.department import Department
from core.exceptions import DatabaseOperationError, ResourceNotFoundError



class DepartmentService:
    """
    Service class for managing Department-related database operations.

    This service provides methods for CRUD (Create, Read, Update, Delete)
    operations on Department entities with robust error handling and type safety.

    Attributes
    ----------
    session : Session
        SQLModel database session for performing database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize DepartmentService with a database session.

        Parameters
        ----------
        session : Session
            SQLModel database session for performing database operations.
        """
        self.session = session

    def create(self, department: Department) -> Department:
        """
        Create a new department in the database.

        Parameters
        ----------
        department : Department
            The department entity to be created.

        Returns
        -------
        Department
            The created department with assigned database ID.

        Raises
        ------
        DatabaseOperationError
            If there's an error during department creation.
        """
        try:
            self.session.add(department)
            self.session.commit()
            self.session.refresh(department)
            return department
        except Exception as e:
            self.session.rollback()
            raise DatabaseOperationError(f'Error creating department: {str(e)}') from e

    def get_by_id(self, department_id: int) -> Department:
        """
        Retrieve a department by its unique identifier.

        Parameters
        ----------
        department_id : int
            The unique identifier of the department.

        Returns
        -------
        Department
            The department with the specified ID.

        Raises
        ------
        ResourceNotFoundError
            If no department is found with the given ID.
        """
        department = self.session.get(Department, department_id)
        if not department:
            raise ResourceNotFoundError(f'Department with ID {department_id} not found')
        return department

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Department]:
        """
        Retrieve a list of departments with optional pagination.

        Parameters
        ----------
        offset : int, optional
            Number of records to skip, by default 0
        limit : int, optional
            Maximum number of records to return, by default 100

        Returns
        -------
        List[Department]
            A list of department entities.
        """
        statement = select(Department).offset(offset).limit(limit)
        results = self.session.exec(statement)
        return list(results.all())

    def update(self, department_id: int, department_update: Department) -> Department:
        """
        Update an existing department.

        Parameters
        ----------
        department_id : int
            The unique identifier of the department to update.
        department_update : Department
            The updated department data.

        Returns
        -------
        Department
            The updated department entity.

        Raises
        ------
        ResourceNotFoundError
            If no department is found with the given ID.
        DatabaseOperationError
            If there's an error during department update.
        """
        try:
            existing_department = self.get_by_id(department_id)
            for key, value in department_update.dict(exclude_unset=True).items():
                setattr(existing_department, key, value)

            self.session.add(existing_department)
            self.session.commit()
            self.session.refresh(existing_department)
            return existing_department
        except Exception as e:
            self.session.rollback()
            raise DatabaseOperationError(f'Error updating department: {str(e)}') from e

    def delete(self, department_id: int) -> None:
        """
        Delete a department by its unique identifier.

        Parameters
        ----------
        department_id : int
            The unique identifier of the department to delete.

        Raises
        ------
        ResourceNotFoundError
            If no department is found with the given ID.
        DatabaseOperationError
            If there's an error during department deletion.
        """
        department = self.get_by_id(department_id)
        if not department:
            raise ResourceNotFoundError(f'Department with ID {department_id} not found')

        try:
            self.session.delete(department)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise DatabaseOperationError(f'Error deleting department: {str(e)}') from e
