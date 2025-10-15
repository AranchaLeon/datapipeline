"""
This script monitors an Azure Blob Storage container for new CSV files and triggers ETL processing.

Usage:
    python init_bucket.py

Main logic:
    - Connects to Azure Blob Storage using environment variables.
    - Creates the container if it does not exist.
    - Continuously polls for new blobs not in the processed/ folder and with .csv extension.
    - For each new CSV blob, runs the ETL pipeline script (main.py) with the blob name as argument.
    - Logs errors and waits between polling cycles.
"""
import os
import subprocess
import tempfile
import time

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient

from src.etl_pipeline.utils.env_vars import EnvConfig
from src.etl_pipeline.utils.logger import get_logger

logger = get_logger()
config = EnvConfig()
config.validate()

connection_str = config.az_connection_string
blob_service_client = BlobServiceClient.from_connection_string(connection_str)

# Check or create container
container_client = blob_service_client.get_container_client(config.az_container_name)
try:
    container_client.create_container()
except ResourceExistsError:
    pass


while True:
    try:
        blob_list = container_client.list_blobs()
    except Exception as e:
        logger.error(f"Error listing blobs: {e}")
        time.sleep(5)
        continue

    for blob in blob_list:
        name = blob.name
        # ignore blobs in the processed/ folder
        if name.startswith(config.processed_prefix):
            # already in processed/success or processed/fail
            continue
        if not name.endswith(".csv"):
            continue

        logger.info(f"New blob detected: {name}")
        result = subprocess.run(["python", "src/etl_pipeline/main.py", name])

    time.sleep(5)
