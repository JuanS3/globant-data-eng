class AppBaseException(Exception):
    """
    Base exception for all custom application exceptions.

    This serves as a parent class for more specific exceptions,
    providing a common base for error handling across the application.
    """

    pass


class DatabaseOperationError(AppBaseException):
    """
    Exception raised for errors during database operations.

    This exception is used when there are issues with database transactions,
    such as creation, update, or deletion of records.

    Attributes
    ----------
    message : str
        Detailed error message describing the database operation failure.
    """

    def __init__(self, message: str):
        """
        Initialize the DatabaseOperationError.

        Parameters
        ----------
        message : str
            A descriptive error message about the database operation failure.
        """
        self.message = message
        super().__init__(self.message)


class ResourceNotFoundError(AppBaseException):
    """
    Exception raised when a requested resource is not found.

    This exception is typically used when attempting to retrieve
    a record that does not exist in the database.

    Attributes
    ----------
    resource_type : str
        The type of resource that was not found (e.g., 'Employee', 'Department').
    resource_id : int or str
        The identifier of the resource that could not be found.
    """

    def __init__(self, message: str):
        """
        Initialize the ResourceNotFoundError.

        Parameters
        ----------
        message : str
            A descriptive error message about the missing resource.
        """
        self.message = message
        super().__init__(self.message)


class ValidationError(AppBaseException):
    """
    Exception raised for data validation failures.

    This exception is used when input data does not meet
    the required validation criteria.

    Attributes
    ----------
    errors : dict
        A dictionary containing validation error details.
    """

    def __init__(self, errors: dict):
        """
        Initialize the ValidationError.

        Parameters
        ----------
        errors : dict
            A dictionary of validation errors, where keys are field names
            and values are lists of error messages.
        """
        self.errors = errors
        super().__init__(str(errors))


class AuthenticationError(AppBaseException):
    """
    Exception raised for authentication-related issues.

    This exception is used when there are problems with user authentication,
    such as invalid credentials or unauthorized access.
    """

    def __init__(self, message: str = 'Authentication failed'):
        """
        Initialize the AuthenticationError.

        Parameters
        ----------
        message : str, optional
            A descriptive error message about the authentication failure.
            Defaults to "Authentication failed".
        """
        self.message = message
        super().__init__(self.message)
