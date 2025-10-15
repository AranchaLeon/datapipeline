import pandas as pd
from sqlalchemy import create_engine
from utils.env_vars import EnvConfig
from utils.logger import get_logger

logger = get_logger()
config = EnvConfig()


def load_df_to_sql(df: pd.DataFrame, table_name: str) -> None:
    """
    Loads a DataFrame into the specified SQL table.
    Returns True if successful, False if failed.
    """
    if df is None or df.empty:
        logger.warning(f"No data for {table_name}.")
        return False

    try:
        engine = get_postgres_engine(config)

        # Batch size for concurrent loading
        batch_size = 1000
        num_records = len(df)
        batches = [
            df.iloc[i:i + batch_size]
            for i in range(0, num_records, batch_size)
        ]

        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = []

        with ThreadPoolExecutor() as executor:
            future_to_batch = {
                executor.submit(
                    lambda batch: batch.to_sql(
                        name=table_name,
                        con=engine,
                        if_exists="append",
                        index=False,
                        method="multi",
                    ),
                    batch,
                ): batch
                for batch in batches
            }
            for future in as_completed(future_to_batch):
                try:
                    future.result()
                    results.append(True)
                except Exception as e:
                    logger.error(
                        f"Error loading batch into table {table_name}: {e}"
                    )
                    results.append(False)
        if all(results):
            logger.info(
                f"Loaded chunk. Loaded {num_records} records into "
                f"{table_name} concurrently."
            )
            return True
        else:
            logger.error(f"Some batches failed to load into {table_name}.")
            return False
    except Exception as e:
        logger.error(f"Error loading into table {table_name}: {e}")
        return False


def get_postgres_engine(config: EnvConfig):
    """
    Creates and returns a SQLAlchemy engine for Postgres connection.
    Args:
        config: Instance of EnvConfig with connection details.
    Returns:
        engine: SQLAlchemy engine
    """

    user = config.postgres_user
    password = config.postgres_password
    db = config.postgres_db
    host = config.postgres_host
    port = config.postgres_port
    sslmode = getattr(config, "postgres_sslmode", None)  # optional

    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

    connect_args = {}
    if sslmode:
        connect_args["sslmode"] = sslmode

    return create_engine(conn_str, connect_args=connect_args)
