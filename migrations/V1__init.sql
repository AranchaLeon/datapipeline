-- =====================================================================
-- Flyway Migration Script
-- Version: V1
-- Description: Create initial schema for sales data pipeline
-- =====================================================================

-- =====================================================
-- Table: sales
-- =====================================================
CREATE TABLE IF NOT EXISTS sales (
    sale_id         SERIAL PRIMARY KEY,
    transaction_id  VARCHAR(100) UNIQUE NOT NULL,
    customer_id     VARCHAR(100) NOT NULL,
    product_id      VARCHAR(100) NOT NULL,
    store_id        VARCHAR(100) NOT NULL,
    quantity        INTEGER NOT NULL,
    unit_price      NUMERIC(10,2) NOT NULL,
    discount        NUMERIC(4,2) DEFAULT 0,
    total_amount    NUMERIC(12,2) NOT NULL,
    payment_method  VARCHAR(50),
    sale_date       DATE NOT NULL,
    sale_time       TIME NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- End of Script
-- =====================================================
