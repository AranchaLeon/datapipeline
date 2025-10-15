from typing import Optional

import numpy as np
import pandas as pd
from cryptography.fernet import Fernet
from utils.env_vars import EnvConfig
from utils.logger import get_logger
from utils.mapping import ColumnMapper, sales_column_mapping

from src.etl_pipeline.utils.csv_schemas import CSV_SCHEMAS
from src.etl_pipeline.utils.table_schemas import SALES_SQLALCHEMY_SCHEMA
from src.etl_pipeline.utils.utils import encrypt_column

logger = get_logger()
config = EnvConfig()


def transform_sales_data(df_raw: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Transform raw sales CSV data into a cleaned and ready-to-load DataFrame.
    Steps:
        1. Validate CSV structure
        2. Apply column mapping
        3. Handle missing values and defaults
        4. Encrypt sensitive columns
        5. Calculate derived columns
        6. Normalize and standardize
        7. Filter invalid rows
        8. Prepare DataFrame for SQL load
    """
    if df_raw is None or df_raw.empty:
        logger.warning("Input DataFrame is None or empty. "
                       "No data to transform.")
        return None

    try:
        # 1. Validate CSV structure
        sales_schema = CSV_SCHEMAS["sales"]
        required_columns = [
            col for col, meta in sales_schema.items()
            if meta.get("required", False)
        ]
        missing_required = [
            col for col in required_columns
            if col not in df_raw.columns
        ]
        extra = [col for col in df_raw.columns if col not in sales_schema]
        if missing_required:
            logger.error(f"Missing required columns: {missing_required}")
            raise ValueError(f"Required columns missing: {missing_required}")
        if extra:
            logger.warning(f"Unexpected columns in DataFrame: {extra}")

        # 2. Apply column mapping
        mapper = ColumnMapper(sales_column_mapping)
        df = mapper.apply(df_raw)

        # 3. Handle missing values and defaults
        df["discount"] = df.get("discount", pd.Series(0)).fillna(0)
        df["total_amount"] = df.get("total_amount", pd.Series(np.nan))
        df["total_amount"] = df["total_amount"].fillna(
            round(
                df["quantity"] * df["unit_price"] * (1 - df["discount"]),
                2
            )
        )

        # 4. Encrypt columns flagged in SALES_SQLALCHEMY_SCHEMA
        fernet_key = config.fernet_key  # 32-byte base64
        fernet = Fernet(fernet_key.encode()) if fernet_key else None
        for col_meta in SALES_SQLALCHEMY_SCHEMA["columns"]:
            col = col_meta["name"]
            if col_meta.get("encrypt", False) and col in df.columns:
                df[col] = encrypt_column(df[col], fernet)

        # 5. Normalize string columns
        string_cols = [
            col_meta["name"]
            for col_meta in SALES_SQLALCHEMY_SCHEMA["columns"]
            if (
                col_meta["type"] == "String"
                and col_meta["name"] in df.columns
            )
        ]
        for col in string_cols:
            df[col] = df[col].astype(str).str.strip().str.lower()

        # 6. Filter invalid rows
        df = df[(df["quantity"] > 0) & (df["unit_price"] >= 0)]
        if df.empty:
            logger.warning("0 rows after validation. No data to load.")
            return None

        # 7. Select only required SQL columns
        required_columns = [
            col_meta["name"]
            for col_meta in SALES_SQLALCHEMY_SCHEMA["columns"]
            if col_meta.get("required", False)
        ]
        missing_sql_cols = [
            col for col in required_columns
            if col not in df.columns
        ]
        if missing_sql_cols:
            logger.error(
                "Missing required SQL columns after transformation: "
                f"{missing_sql_cols}"
            )
            raise ValueError(f"Missing required columns: {missing_sql_cols}")

        df_transformed = df[required_columns].copy()

        logger.info(
            f"Transformed chunk. Output {len(df_transformed)} rows"
        )
        return df_transformed

    except Exception as e:
        logger.error(
            f"Error during sales data transformation: {e}"
        )
        return None
