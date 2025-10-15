CSV_SCHEMAS = {
    "sales": {
        "transaction_id": {"type": str, "required": True},
        "customer_id": {"type": str, "required": True},
        "product_id": {"type": str, "required": True},
        "store_id": {"type": str, "required": True},
        "quantity": {"type": (int, float), "required": True},
        "unit_price": {"type": (int, float), "required": True},
        "discount": {"type": (float, int), "required": False},
        "total_amount": {"type": (float, int), "required": False},
        "payment_method": {"type": str, "required": True},
        "timestamp": {"type": str, "required": True},
    },
    "suppliers": {},
    "products": {},
    "customers": {},
    "stores": {},
}
