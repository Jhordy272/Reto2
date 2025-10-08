-- Script to create products table

CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    stock INTEGER NOT NULL,
    price DOUBLE PRECISION NOT NULL
);

-- Insert 2 products
INSERT INTO products (name, description, stock, price) VALUES
('Laptop Dell XPS 13', 'Laptop, 16GB RAM, 512GB SSD', 15, 1299.99),
('Mouse Logitech MX Master 3', 'Mouse', 50, 99.99);
