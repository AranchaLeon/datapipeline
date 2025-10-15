from io import StringIO

import pandas as pd
from utils.env_vars import EnvConfig
from utils.logger import get_logger

from src.etl_pipeline.utils.utils import create_blob_client

logger = get_logger()
config = EnvConfig()


def extract_data_from_azure_blob_stream(blob_name: str, chunk_size: int):
    """
    Stream a CSV blob from Azure Storage and yield pandas DataFrames
    in chunks of exact rows. Does not load the entire blob into memory.

    Args:
        blob_name (str): Name of the blob in Azure container.
        chunk_size (int): Number of rows per chunk.

    Yields:
        pd.DataFrame: DataFrame containing up to chunk_size rows.
    """
    try:
        # Create blob client and open stream
        blob_client = create_blob_client(blob_name)
        stream_downloader = blob_client.download_blob()

        # Initialize line buffer
        lines = []
        header = None
        chunk_index = 1

        # Iterate over raw bytes from Azure in chunks
        for byte_chunk in stream_downloader.chunks():
            # Decode bytes to string lines
            text_chunk = byte_chunk.decode("utf-8")
            for line in text_chunk.splitlines():
                if not line.strip():
                    continue  # skip empty lines

                if header is None:
                    # First non-empty line is the CSV header
                    header = line
                    continue

                lines.append(line)
                # If we've collected enough lines, yield a DataFrame
                if len(lines) >= chunk_size:
                    csv_buffer = StringIO("\n".join([header] + lines))
                    df_chunk = pd.read_csv(csv_buffer)
                    logger.info(
                        f"Extracted chunk {chunk_index}. "
                        f"Output {len(df_chunk)} rows"
                    )
                    yield df_chunk
                    lines = []
                    chunk_index += 1

        # Yield remaining lines
        if lines:
            csv_buffer = StringIO("\n".join([header] + lines))
            df_chunk = pd.read_csv(csv_buffer)
            logger.info(
                f"Yielding final stream chunk {chunk_index} "
                f"with {len(df_chunk)} rows"
            )
            yield df_chunk

    except Exception as e:
        logger.error(f"Error processing blob '{blob_name}' from Azure: {e}")
        raise RuntimeError(
            f"Exception: from_storage.extract_data_from_azure_blob_stream: {e}"
        )
