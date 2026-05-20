class DatabaseUnavailableError(RuntimeError):
    """Raised when the application is configured to serve data only from PostgreSQL."""

