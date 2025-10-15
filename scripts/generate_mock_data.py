"""
This script generates mock sales data as a CSV file for testing ETL pipelines.

Usage:
    python generate_mock_data.py [num_rows] [start_date] [end_date]

Arguments:
    num_rows (int, optional): Number of rows to generate. Default is 100.
    start_date (str, optional): Start datetime in '%Y-%m-%d %H:%M:%S' format.
    end_date (str, optional): End datetime in '%Y-%m-%d %H:%M:%S' format.
"""
import csv
import os
import random
import sys
from uuid import uuid4
from datetime import datetime, timedelta


def random_timestamp(start, end):
    """
    Generate a random timestamp between two datetime objects.
    
    Args:
        start (datetime): Start datetime.
        end (datetime): End datetime.
    
    Returns:
        datetime: Random datetime between start and end.
    """
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def main():
    """
    Generates mock sales data and writes it to a CSV file.
    Reads optional command-line arguments for number of rows and date range.
    The output file is named with a timestamp and saved in the ../data directory.
    """
    

    os.makedirs("../data", exist_ok=True)
    execution_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"../data/sales_{execution_timestamp}.csv"
    customers = ["CUST-001", "CUST-002", "CUST-003", "CUST-004", "CUST-005"]
    products = [
        "PROD-001",
        "PROD-002",
        "PROD-003",
        "PROD-004",
        "PROD-005",
        "PROD-006",
        "PROD-007",
        "PROD-008",
    ]
    stores = ["STORE-001", "STORE-002", "STORE-003", "STORE-004", "STORE-005"]
    payment_methods = ["credit card", "debit card", "paypal", "cash"]
    args = sys.argv[1:]
    num_rows = 100
    start = datetime(2025, 10, 9, 8, 0, 0)
    end = datetime(2025, 10, 12, 22, 0, 0)
    if len(args) > 0:
        try:
            num_rows = int(args[0])
        except ValueError:
            print(f"Invalid argument: {args[0]}. Using default value: {num_rows}.")
    if len(args) > 1:
        try:
            start = datetime.strptime(args[1], "%Y-%m-%d %H:%M:%S")
        except Exception:
            print(f"Invalid start date: {args[1]}. Using default {start}.")
    if len(args) > 2:
        try:
            end = datetime.strptime(args[2], "%Y-%m-%d %H:%M:%S")
        except Exception:
            print(f"Invalid end date: {args[2]}. Using default {end}.")

    # Generate sorted timestamps to ensure chronological order
    timestamps = [random_timestamp(start, end) for _ in range(num_rows)]
    timestamps.sort()

    rows = []
    for i in range(num_rows):
        transaction_id = f"TX-{uuid4()}"
        customer_id = random.choice(customers)
        product_id = random.choice(products)
        store_id = random.choice(stores)
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(15.0, 600.0), 2)
        discount = random.choice([0, 0.05, 0.10, 0.15, None])
        payment_method = random.choice(payment_methods)
        timestamp = timestamps[i]
        total_amount = round(quantity * unit_price * (1 - (discount or 0)), 2)
        row = {
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "product_id": product_id,
            "store_id": store_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount if discount is not None else "",
            "total_amount": total_amount,
            "payment_method": payment_method,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        rows.append(row)
    fieldnames = [
        "transaction_id",
        "customer_id",
        "product_id",
        "store_id",
        "quantity",
        "unit_price",
        "discount",
        "total_amount",
        "payment_method",
        "timestamp",
    ]
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ CSV file generated successfully: {output_file}")


if __name__ == "__main__":
    main()
