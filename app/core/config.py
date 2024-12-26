from typing import Optional
from sqlmodel import SQLModel, Field, create_engine
import os


class DatabaseSettings(SQLModel):
    """
    Database configuration settings using SQLModel.

    Provides a structured way to manage database connection parameters
    and create database engine configurations.
    """

    # Database Connection Parameters
    host: str = Field(default=os.getenv("DATABASE_HOST", "localhost"))
    port: int = Field(default=int(os.getenv("DATABASE_PORT", 5432)))
    user: str = Field(default=os.getenv("DATABASE_USER", "postgres"))
    password: str = Field(default=os.getenv("DATABASE_PASSWORD", "postgres"))
    database: str = Field(default=os.getenv("DATABASE_NAME", "globant_data_eng"))

    @property
    def database_url(self) -> str:
        """
        Generate the full PostgreSQL database connection URL.

        Returns
        -------
        str
            Formatted database connection string.
        """
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def create_engine(self, echo: bool = False):
        """
        Create a SQLAlchemy engine with specific configuration.

        Parameters
        ----------
        echo : bool, optional
            Enable SQL statement logging, by default False

        Returns
        -------
        Engine
            Configured database engine
        """
        return create_engine(
            self.database_url,
            echo=echo,
        )


class AppSettings(SQLModel):
    """
    Application-wide configuration settings.

    Manages various application-level configurations
    using SQLModel for type safety and validation.
    """

    # Application Metadata
    name: str = Field(default="Globant Data Engineering Challenge")
    version: str = Field(default="0.1.0")
    description: str = Field(default="API for processing and analyzing employee data")

    # Environment Configuration
    environment: str = Field(default=os.getenv("APP_ENV", "development"))
    debug: bool = Field(default=os.getenv("DEBUG", "True").lower() == "true")

    # Logging and Performance
    log_level: str = Field(default=os.getenv("LOG_LEVEL", "INFO"))
    sql_echo: bool = Field(default=os.getenv("SQL_ECHO", "False").lower() == "true")

    # Security Settings
    secret_key: Optional[str] = Field(default=os.getenv("SECRET_KEY"))

    @property
    def is_production(self) -> bool:
        """
        Check if the application is running in production mode.

        Returns
        -------
        bool
            True if environment is production, False otherwise.
        """
        return self.environment.lower() == "production"


# Create singleton instances
settings = DatabaseSettings()
app_settings = AppSettings()
