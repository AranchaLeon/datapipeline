import os
import sys
import time

from utils.env_vars import EnvConfig
from utils.logger import get_logger

from src.etl_pipeline.extract.from_storage import (
    extract_data_from_azure_blob_stream
)
from src.etl_pipeline.load.to_sql import load_df_to_sql
from src.etl_pipeline.transform.sales_data import transform_sales_data
from src.etl_pipeline.utils.utils import (
    estimate_chunk_size,
    move_blob
)

logger = get_logger()
config = EnvConfig()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python main.py <blob>")
        sys.exit(1)

    blob_name = sys.argv[1]
    logger.info("----- ETL JOB START -----")
    logger.info(f"Processing blob: {blob_name}")

    success = True
    chunk_results = []

    try:
        config.validate()
        timestamp = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        chunk_size = estimate_chunk_size()

        for i, df_chunk in enumerate(
            extract_data_from_azure_blob_stream(blob_name, chunk_size), start=1
        ):
            try:
                df_chunk_processed = transform_sales_data(df_chunk)
                load_success = load_df_to_sql(df_chunk_processed, "sales")
                chunk_results.append({"chunk": i, "success": load_success})

                if not load_success:
                    logger.error(f"Chunk {i} failed to load into SQL")
                    success = False

            except Exception as e:
                logger.error(f"Chunk {i} failed: {e}")
                chunk_results.append({"chunk": i, "success": False})
                success = False

    except Exception as e:
        logger.error(f"ETL job failed: {e}")
        success = False

    finally:
        total_chunks = len(chunk_results)
        succeeded_chunks = sum(r["success"] for r in chunk_results)
        failed_chunks = total_chunks - succeeded_chunks

        logger.info("----- ETL JOB SUMMARY -----")
        logger.info(f"Total chunks processed: {total_chunks}")
        logger.info(f"Chunks succeeded: {succeeded_chunks}")
        logger.info(f"Chunks failed: {failed_chunks}")
        logger.info(f"ETL job status: {'SUCCESS' if success else 'FAILURE'}")

        # Move the blob to processed/success or processed/failure
        base, ext = os.path.splitext(os.path.basename(blob_name))
        dest_prefix = config.success_prefix if success else config.fail_prefix
        dest_blob_name = f"{dest_prefix}{base}_{timestamp}{ext}"

        try:
            move_blob(blob_name, dest_blob_name)
        except Exception as e:
            logger.error(f"Failed to move blob: {e}")

        logger.info("----- ETL JOB END -----")
