import pandas as pd
import psutil
from azure.storage.blob import BlobServiceClient
from utils.env_vars import EnvConfig
from utils.logger import get_logger

logger = get_logger()
config = EnvConfig()


def move_blob(blob_name, dest_blob_name):
    """
    Move a blob from one name to another within the same container.
    Deletes the original blob after copying.
    Args:
        blob_name (str): Source blob name.
        dest_blob_name (str): Destination blob name.
    """
    try:
        container_client = create_container_client()
        blob_client = container_client.get_blob_client(blob_name)
        dest_blob_client = container_client.get_blob_client(dest_blob_name)

        source_url = blob_client.url
        dest_blob_client.start_copy_from_url(source_url)
        blob_client.delete_blob()
        logger.info(f"Blob '{blob_name}' moved to '{dest_blob_name}'")
    except Exception as e:
        logger.error(f"Error moving blob {blob_name} to {dest_blob_name}: {e}")


def estimate_chunk_size() -> int:
    """
    Estimate the optimal chunk size for processing data based on environment variables and available memory.
    Returns:
        int: Estimated chunk size (number of rows).
    """
    try:
        if config.environment.lower() == "local":
            chunk_size = int(config.chunk_size)
            logger.info(
                f"Chunk size from local env: {chunk_size} rows (local)"
            )
        else:
            env_fraction = config.desired_chunk_fraction
            env_row_size = config.avg_row_size_bytes

            mem = psutil.virtual_memory()
            available = mem.available
            chunk_mem = int(available * float(env_fraction))
            chunk_size = max(1000, chunk_mem // int(env_row_size))
            logger.info(
                f"Chunk size estimated: {chunk_size} rows (using ~"
                f"{chunk_mem//1024//1024}MB RAM per chunk)"
            )

        return chunk_size
    except Exception as e:
        logger.error(f"Error estimating chunk size: {e}")
        return 10000  # fallback default


def create_container_client():
    """
    Create and return a ContainerClient for the configured Azure Blob container.
    Returns:
        ContainerClient: Azure Blob ContainerClient instance.
    Raises:
        RuntimeError: If the client cannot be created.
    """
    try:
        connection_str = config.az_connection_string
        container_name = config.az_container_name
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_str
        )
        return blob_service_client.get_container_client(container_name)
    except Exception as e:
        logger.error(
            f"Error creating ContainerClient for '{container_name}': {e}"
        )
        raise RuntimeError(
            f"Error creating ContainerClient for '{container_name}': {e}"
        )


def create_blob_client(blob_name: str):
    """
    Create and return a BlobClient for a specific blob in the configured container.
    Args:
        blob_name (str): Name of the blob.
    Returns:
        BlobClient: Azure BlobClient instance.
    Raises:
        RuntimeError: If the client cannot be created.
    """
    try:
        container_client = create_container_client()
        return container_client.get_blob_client(blob_name)
    except Exception as e:
        logger.error(f"Error creating BlobClient for '{blob_name}': {e}")
        raise RuntimeError(f"Error creating BlobClient for '{blob_name}': {e}")


def encrypt_column(series: pd.Series, fernet=None) -> pd.Series:
    """
    Encrypt a pandas Series using Fernet. Return hexadecimal strings.
    """
    if fernet is None:
        return series
    return series.astype(str).apply(
        lambda x: fernet.encrypt(x.encode()).decode()
    )
