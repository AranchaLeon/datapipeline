"""
This script uploads a CSV file to an Azurite (Azure Blob Storage emulator) container.
It reads connection details from environment variables and handles errors gracefully.

Usage:
    python upload_to_azurite.py [file_path]
    If no file_path is provided, the most recent CSV in ../data is used.
"""

import glob
import logging
import os
import sys

from azure.storage.blob import BlobServiceClient

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger("upload_to_azurite")

AZ_BLOB_URL = "http://127.0.0.1:10000/devstoreaccount1"
AZ_ACCOUNT_NAME = "devstoreaccount1"
AZ_ACCOUNT_KEY = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
CONTAINER_NAME = "mycontainer"


def upload_file(file_path):
    """
    Uploads a file to the Azurite blob container.
    Creates the container if it does not exist.
    Handles errors for missing files, environment variables, connection issues, and upload failures.

    Args:
        file_path (str): Path to the file to upload.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        logger.error(f"Archivo '{file_path}' no encontrado.")
        return
    connection_str = (
        f"DefaultEndpointsProtocol=http;"
        f"AccountName={AZ_ACCOUNT_NAME};"
        f"AccountKey={AZ_ACCOUNT_KEY};"
        f"BlobEndpoint={AZ_BLOB_URL};"
    )
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_str)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    except Exception as e:
        logger.error(f"Error connecting to Azurite: {e}")
        return

    try:
        container_client.create_container()
        logger.info(f"Container '{CONTAINER_NAME}' created.")
    except Exception as e:
        if "ContainerAlreadyExists" in str(e):
            logger.info(f"Container '{CONTAINER_NAME}' already exists.")
        else:
            logger.error(f"Error creating container: {e}")
            return
        
    blob_name = os.path.basename(file_path)
    try:
        # Create blob client and upload the file
        blob_client = container_client.get_blob_client(blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        logger.info(f"✅ File '{blob_name}' uploaded successfully to Azurite.")
    except Exception as e:
        logger.error(f"Error uploading file '{blob_name}': {e}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Use the file path provided as an argument
        file_path = sys.argv[1]
    else:
        # Otherwise, find the most recent CSV file in ../data
        files = glob.glob("../data/*.csv")
        if not files:
            logger.error("No CSV files found in data.")
            sys.exit(1)
        file_path = max(files, key=os.path.getctime)
        logger.info(f"No file provided, using the most recent: {file_path}")
    upload_file(file_path)
