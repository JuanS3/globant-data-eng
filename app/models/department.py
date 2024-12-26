from sqlmodel import SQLModel, Field


class Department(SQLModel, table=True):
    """
    Represents a department within the organization.

    This model stores information about different departments,
    providing a structured way to categorize and manage organizational units.

    Attributes
    ----------
    id : int
        Unique identifier for the department.
        Serves as the primary key in the database.

    department : str
        The name of the department.
        Represents the specific organizational unit or division.

    Examples
    --------
    >>> dept = Department(id=1, department="Engineering")
    >>> dept.department
    'Engineering'
    """
    __tablename__ = "departments"

    id: int = Field(primary_key=True)
    department: str
