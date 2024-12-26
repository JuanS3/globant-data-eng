from sqlmodel import SQLModel, Field


class Job(SQLModel, table=True):
    """
    Represents a job position in the organization.

    This model stores information about different job titles within the company,
    serving as a reference for employee job classifications.

    Attributes
    ----------
    id : int
        Unique identifier for the job position.
        Serves as the primary key in the database.

    job : str
        The name or title of the job position.
        Represents the specific role or designation within the organization.

    Examples
    --------
    >>> job = Job(id=1, job="Software Engineer")
    >>> job.job
    'Software Engineer'
    """
    __tablename__ = "jobs"

    id: int = Field(default=None, primary_key=True)
    job: str
