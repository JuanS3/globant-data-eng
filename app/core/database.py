from sqlmodel import SQLModel, Session
from typing import Generator

from core.config import settings

# Create SQLModel engine with connection pooling disabled
engine = settings.create_engine()


def init_db() -> None:
    """
    Initialize the database by creating all tables defined in SQLModel models.

    This function creates the database schema based on the SQLModel table definitions.
    It should be called during application startup to ensure all tables are created.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Create and yield a database session.

    This function is typically used as a dependency in FastAPI to provide
    database sessions for each request.

    Yields
    ------
    Session
        A SQLModel database session that can be used for database operations.

    Examples
    --------
    >>> with next(get_session()) as session:
    ...     # Perform database operations
    ...     result = session.exec(select(SomeModel))
    """
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
