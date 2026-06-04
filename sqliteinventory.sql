-- Enable Foreign Key support in SQLite (Crucial step!)
PRAGMA foreign_keys = ON;

-- 1. PRODUCT TABLE (Master list of what you sell)
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT
);

-- 2. INVENTORY TABLE (Tracks stock levels for each product)
CREATE TABLE inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity_in_stock INTEGER DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- 3. CLIENT TABLE (Information about your buyers)
CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT
);

-- 4. SALES TABLE (Tracks transactions mapping clients to products)
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO products (product_name, price, category) VALUES 
('Wireless Mouse', 25.00, 'Electronics'),
('Mechanical Keyboard', 85.50, 'Electronics'),
('Ergonomic Chair', 200.00, 'Office');

-- Add Initial Inventory
INSERT INTO inventory (product_id, quantity_in_stock) VALUES 
(1, 50), -- 50 mice
(2, 20), -- 20 keyboards
(3, 5);  -- 5 chairs

-- Add Clients
INSERT INTO clients (first_name, last_name, email, phone) VALUES 
('John', 'Doe', 'john@email.com', '555-0199'),
('Jane', 'Smith', 'jane@email.com', '555-0144');

-- Record Sales
INSERT INTO sales (client_id, product_id, quantity_sold, total_amount) VALUES 
(1, 1, 2, 50.00),  -- John Doe bought 2 Wireless Mice
(2, 3, 1, 200.00); -- Jane Smith bought 1 Ergonomic Chair

-- See a complete sales receipt report joining all tables
SELECT 
    s.sale_id,
    c.first_name || ' ' || c.last_name AS client_name,
    p.product_name,
    s.quantity_sold,
    s.total_amount,
    s.sale_date
FROM sales s
JOIN clients c ON s.client_id = c.client_id
JOIN products p ON s.product_id = p.product_id;