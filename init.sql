CREATE DATABASE IF NOT EXISTS ecomm_db;
USE ecomm_db;
CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), price DECIMAL(10,2), stock INT);
INSERT INTO products (name, price, stock) VALUES ('Laptop', 999.99, 10), ('Smartphone', 499.50, 20), ('Headphones', 89.00, 50);

CREATE TABLE cart_items (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, product_id INT, quantity INT);
CREATE TABLE orders (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, status VARCHAR(20) DEFAULT 'Pending');