-- =====================================================================
-- Flyway Migration Script
-- Version: V2
-- Description: Insert mock data into sales schema
-- =====================================================================

-- =====================================================
-- Suppliers
-- =====================================================
INSERT INTO suppliers (supplier_id, name, country, contact_email) VALUES
('SUP-001', 'TechWorld Distribution', 'Spain', 'sales@techworld.es'),
('SUP-002', 'HomeStyle Ltd.', 'France', 'info@homestyle.fr'),
('SUP-003', 'GadgetPro Europe', 'Germany', 'contact@gadgetpro.de'),
('SUP-004', 'EcoLife Imports', 'Italy', 'hello@ecolife.it')
ON CONFLICT (supplier_id) DO NOTHING;

-- =====================================================
-- Products
-- =====================================================
INSERT INTO products (product_id, name, category, current_price, cost, supplier_id, stock) VALUES
('PROD-001', 'Wireless Mouse', 'Electronics', 19.99, 9.50, 'SUP-001', 150),
('PROD-002', 'Mechanical Keyboard', 'Electronics', 79.99, 42.00, 'SUP-001', 80),
('PROD-003', 'Office Chair', 'Furniture', 149.99, 95.00, 'SUP-002', 40),
('PROD-004', 'Desk Lamp', 'Lighting', 39.99, 18.50, 'SUP-002', 70),
('PROD-005', 'Smartphone X1', 'Electronics', 599.99, 420.00, 'SUP-003', 25),
('PROD-006', 'Coffee Maker', 'Appliances', 89.99, 54.00, 'SUP-004', 60),
('PROD-007', 'Noise Cancelling Headphones', 'Electronics', 199.99, 120.00, 'SUP-003', 30),
('PROD-008', 'Standing Desk', 'Furniture', 299.99, 210.00, 'SUP-002', 15)
ON CONFLICT (product_id) DO NOTHING;

-- =====================================================
-- Customers
-- =====================================================
INSERT INTO customers (customer_id, first_name, last_name, email, phone, join_date, country, city) VALUES
('CUST-001', 'Laura', 'Martínez', 'laura.martinez@example.com', '+34 600123456', '2024-05-11', 'Spain', 'Madrid'),
('CUST-002', 'Carlos', 'López', 'carlos.lopez@example.com', '+34 600654321', '2024-06-22', 'Spain', 'Barcelona'),
('CUST-003', 'Anna', 'Dupont', 'anna.dupont@example.fr', '+33 612345678', '2024-07-10', 'France', 'Paris'),
('CUST-004', 'Julia', 'Weber', 'julia.weber@example.de', '+49 151234567', '2024-08-01', 'Germany', 'Berlin'),
('CUST-005', 'Marco', 'Rossi', 'marco.rossi@example.it', '+39 345678901', '2024-09-15', 'Italy', 'Milan')
ON CONFLICT (customer_id) DO NOTHING;

-- =====================================================
-- Stores
-- =====================================================
INSERT INTO stores (store_id, name, city, country) VALUES
('STORE-001', 'TechWorld Madrid', 'Madrid', 'Spain'),
('STORE-002', 'TechWorld Barcelona', 'Barcelona', 'Spain'),
('STORE-003', 'HomeStyle Paris', 'Paris', 'France'),
('STORE-004', 'GadgetPro Berlin', 'Berlin', 'Germany'),
('STORE-005', 'EcoLife Milan', 'Milan', 'Italy')
ON CONFLICT (store_id) DO NOTHING;

-- =====================================================
-- Sales
-- =====================================================
INSERT INTO sales (
    transaction_id, customer_id, product_id, store_id, quantity, unit_price, discount,
    total_amount, payment_method, sale_date, sale_time
) VALUES
('TX-00000001-0000-0000-0000-000000000001', 'CUST-001', 'PROD-001', 'STORE-001', 2, 19.99, 0.00, 39.98, 'credit card', '2025-10-10', '10:45:12'),
('TX-00000002-0000-0000-0000-000000000002', 'CUST-002', 'PROD-002', 'STORE-002', 1, 79.99, 0.10, 71.99, 'paypal', '2025-10-10', '11:05:44'),
('TX-00000003-0000-0000-0000-000000000003', 'CUST-003', 'PROD-004', 'STORE-003', 3, 39.99, 0.05, 113.97, 'cash', '2025-10-10', '12:15:22'),
('TX-00000004-0000-0000-0000-000000000004', 'CUST-004', 'PROD-005', 'STORE-004', 1, 599.99, 0.00, 599.99, 'credit card', '2025-10-10', '13:22:58'),
('TX-00000005-0000-0000-0000-000000000005', 'CUST-005', 'PROD-006', 'STORE-005', 2, 89.99, 0.15, 152.98, 'sebit card', '2025-10-10', '14:18:05'),
('TX-00000006-0000-0000-0000-000000000006', 'CUST-002', 'PROD-007', 'STORE-002', 1, 199.99, 0.00, 199.99, 'credit card', '2025-10-10', '15:03:41'),
('TX-00000007-0000-0000-0000-000000000007', 'CUST-001', 'PROD-008', 'STORE-001', 1, 299.99, 0.20, 239.99, 'paypal', '2025-10-11', '09:12:07'),
('TX-00000008-0000-0000-0000-000000000008', 'CUST-003', 'PROD-003', 'STORE-003', 2, 149.99, 0.05, 284.98, 'credit card', '2025-10-11', '10:47:30'),
('TX-00000009-0000-0000-0000-000000000009', 'CUST-004', 'PROD-002', 'STORE-004', 1, 79.99, 0.00, 79.99, 'cash', '2025-10-11', '11:34:19'),
('TX-00000010-0000-0000-0000-000000000010', 'CUST-005', 'PROD-006', 'STORE-005', 3, 89.99, 0.10, 242.97, 'sebit card', '2025-10-11', '12:56:03')
ON CONFLICT (transaction_id) DO NOTHING;

-- =====================================================
-- End of Script
-- =====================================================
