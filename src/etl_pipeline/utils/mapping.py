import pandas as pd

sales_column_mapping = {
    "transaction_id": "transaction_id",
    "customer_id": "customer_id",
    "product_id": "product_id",
    "store_id": "store_id",
    "quantity": "quantity",
    "unit_price": "unit_price",
    "discount": "discount",
    "total_amount": "total_amount",
    "payment_method": "payment_method",
    "timestamp": ["sale_date", "sale_time"],
}


class ColumnMapper:
    def __init__(self, mapping: dict):
        """
        Initialize ColumnMapper with a mapping dict that defines CSV to SQL column mapping.
        Args:
            mapping (dict): Dictionary mapping CSV columns to SQL columns or lists of columns.
        """

        self.mapping = mapping

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply the column mapping to a DataFrame, handling direct and multi-column mappings.
        Args:
            df (pd.DataFrame): Input DataFrame with CSV columns.
        Returns:
            pd.DataFrame: DataFrame with columns mapped for SQL loading.
        """
        
        df_mapped = df.copy()

        for csv_col, sql_target in self.mapping.items():
            if csv_col not in df.columns:
                continue

            # Direct mapping
            if isinstance(sql_target, str):
                df_mapped.rename(columns={csv_col: sql_target}, inplace=True)

            # Multiple target columns
            elif isinstance(sql_target, list):
                if csv_col == "timestamp":
                    df_mapped["sale_date"] = pd.to_datetime(
                        df[csv_col]
                    ).dt.date
                    df_mapped["sale_time"] = pd.to_datetime(
                        df[csv_col]
                    ).dt.time

        return df_mapped
