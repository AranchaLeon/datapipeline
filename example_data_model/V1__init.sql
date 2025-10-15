-- =====================================================================
-- Flyway Migration Script
-- Version: V1
-- Description: Create initial schema for sales data pipeline
-- =====================================================================

-- =====================================================
-- Table: suppliers
-- =====================================================
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id     VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    country         VARCHAR(50),
    contact_email   VARCHAR(100) UNIQUE
);

-- =====================================================
-- Table: products
-- =====================================================
CREATE TABLE IF NOT EXISTS products (
    product_id      VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    category        VARCHAR(50),
    current_price   NUMERIC(10,2) NOT NULL,
    cost            NUMERIC(10,2),
    supplier_id     VARCHAR(50),
    stock           INTEGER DEFAULT 0,
    CONSTRAINT fk_product_supplier FOREIGN KEY (supplier_id)
        REFERENCES suppliers (supplier_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- =====================================================
-- Table: customers
-- =====================================================
CREATE TABLE IF NOT EXISTS customers (
    customer_id     VARCHAR(50) PRIMARY KEY,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(100) UNIQUE,
    phone           VARCHAR(20),
    join_date       DATE DEFAULT CURRENT_DATE,
    country         VARCHAR(50),
    city            VARCHAR(50)
);

-- =====================================================
-- Table: stores
-- =====================================================
CREATE TABLE IF NOT EXISTS stores (
    store_id        VARCHAR(50) PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    city            VARCHAR(50),
    country         VARCHAR(50)
);

-- =====================================================
-- Table: sales
-- =====================================================
CREATE TABLE IF NOT EXISTS sales (
    sale_id         SERIAL PRIMARY KEY,
    transaction_id  VARCHAR(100) UNIQUE NOT NULL,
    customer_id     VARCHAR(100) NOT NULL,
    product_id      VARCHAR(100) NOT NULL,
    store_id        VARCHAR(50) NOT NULL,
    quantity        INTEGER NOT NULL,
    unit_price      NUMERIC(10,2) NOT NULL,
    discount        NUMERIC(4,2) DEFAULT 0,
    total_amount    NUMERIC(12,2) NOT NULL,
    payment_method  VARCHAR(50),
    sale_date       DATE NOT NULL,
    sale_time       TIME NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sale_customer FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_sale_product FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_sale_store FOREIGN KEY (store_id)
        REFERENCES stores (store_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- =====================================================
-- Indexes for sales table
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales (sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales (customer_id);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales (product_id);
CREATE INDEX IF NOT EXISTS idx_sales_store ON sales (store_id);

-- =====================================================
-- End of Script
-- =====================================================
