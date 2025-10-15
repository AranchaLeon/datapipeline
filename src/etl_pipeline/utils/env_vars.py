import os


class EnvConfig:
    REQUIRED_VARS = [
        "ENVIRONMENT",
        "AZ_BLOB_URL",
        "AZ_ACCOUNT_NAME",
        "AZ_ACCOUNT_KEY",
        "AZ_CONTAINER_NAME",
        "AZ_CONNECTION_STRING",
        "DESIRED_CHUNK_FRACTION",
        "AVG_ROW_SIZE_BYTES",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "FERNET_KEY",
        "POSTGRES_SSLMODE"
    ]

    OPTIONAL_VARS = [
        "CHUNK_SIZE",
    ]

    def __init__(self):
        """
        Initialize EnvConfig by loading required and optional environment
        variables. Sets up processed/success/fail prefixes for blob management.
        """
        for var in self.REQUIRED_VARS:
            setattr(self, var.lower(), os.getenv(var))
        for var in self.OPTIONAL_VARS:
            setattr(self, var.lower(), os.getenv(var, None))
        self.processed_prefix = "processed/"
        self.success_prefix = self.processed_prefix + "success/"
        self.fail_prefix = self.processed_prefix + "fail/"

    def validate(self):
        """
        Validate that all required environment variables are set.
        Raises:
            RuntimeError: If any required variable is missing.
        """
        missing = [var for var in self.REQUIRED_VARS if not os.getenv(var)]
        if missing:
            raise RuntimeError(
                f"Missing environment variables: {', '.join(missing)}"
            )
