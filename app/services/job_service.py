from sqlmodel import Session, select

from models.job import Job
from core.exceptions import DatabaseOperationError, ResourceNotFoundError


class JobService:
    """
    Service class for managing Job-related database operations.

    This service provides methods for CRUD (Create, Read, Update, Delete)
    operations on Job entities with robust error handling and type safety.

    Attributes
    ----------
    session : Session
        SQLModel database session for performing database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize JobService with a database session.

        Parameters
        ----------
        session : Session
            SQLModel database session for performing database operations.
        """
        self.session = session

    def create(self, job: Job) -> Job:
        """
        Create a new job in the database.

        Parameters
        ----------
        job : Job
            The job entity to be created.

        Returns
        -------
        Job
            The created job with assigned database ID.

        Raises
        ------
        DatabaseOperationError
            If there's an error during job creation.
        """
        try:
            self.session.add(job)
            self.session.commit()
            self.session.refresh(job)
            return job
        except Exception as e:
            self.session.rollback()
            raise DatabaseOperationError(f'Error creating job: {str(e)}') from e

    def get_by_id(self, job_id: int) -> Job:
        """
        Retrieve a job by its unique identifier.

        Parameters
        ----------
        job_id : int
            The unique identifier of the job.

        Returns
        -------
        Job
            The job with the specified ID.

        Raises
        ------
        ResourceNotFoundError
            If no job is found with the given ID.
        """
        job = self.session.get(Job, job_id)
        if not job:
            raise ResourceNotFoundError(f'Job with ID {job_id} not found')
        return job

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Job]:
        """
        Retrieve a list of jobs with optional pagination.

        Parameters
        ----------
        offset : int, optional
            Number of records to skip, by default 0
        limit : int, optional
            Maximum number of records to return, by default 100

        Returns
        -------
        List[Job]
            A list of job entities.
        """
        statement = select(Job).offset(offset).limit(limit)
        results = self.session.exec(statement)
        return list(results.all())

    def update(self, job_id: int, job_update: Job) -> Job:
        """
        Update an existing job.

        Parameters
        ----------
        job_id : int
            The unique identifier of the job to update.
        job_update : Job
            The updated job data.

        Returns
        -------
        Job
            The updated job entity.

        Raises
        ------
        ResourceNotFoundError
            If no job is found with the given ID.
        DatabaseOperationError
            If there's an error during job update.
        """
        existing_job = self.get_by_id(job_id)

        if not existing_job:
            return None

        try:
            for key, value in job_update.model_dump(exclude_unset=True).items():
                setattr(existing_job, key, value)

            self.session.add(existing_job)
            self.session.commit()
            self.session.refresh(existing_job)
            return existing_job

        except Exception as e:
            self.session.rollback()
            raise DatabaseOperationError(f"Error updating job: {str(e)}") from e

    def delete(self, job_id: int) -> None:
        """
        Delete a job by its unique identifier.

        Parameters
        ----------
        job_id : int
            The unique identifier of the job to delete.

        Raises
        ------
        ResourceNotFoundError
            If no job is found with the given ID.
        DatabaseOperationError
            If there's an error during job deletion.
        """
        try:
            job = self.get_by_id(job_id)
            self.session.delete(job)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise DatabaseOperationError(f"Error deleting job: {str(e)}") from e
