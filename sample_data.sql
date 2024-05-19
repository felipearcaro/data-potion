-- Create a database
CREATE DATABASE IF NOT EXISTS sales_data;

-- Create a schema
CREATE SCHEMA IF NOT EXISTS sales_data.customer_info;

-- Create customers table
CREATE TABLE IF NOT EXISTS sales_data.customer_info.customers (
    customer_id INT PRIMARY KEY COMMENT 'Unique identifier for each customer',
    first_name STRING COMMENT 'First name of the customer',
    last_name STRING COMMENT 'Last name of the customer',
    email STRING
);

-- Create products table
CREATE TABLE IF NOT EXISTS sales_data.customer_info.products (
    product_id INT PRIMARY KEY COMMENT 'Unique identifier for each product',
    product_name STRING,
    price FLOAT COMMENT 'Price of the product'
);

-- Create orders table
-- Create orders table
CREATE TABLE IF NOT EXISTS sales_data.customer_info.orders (
    order_id INT PRIMARY KEY COMMENT 'Unique identifier for each order',
    customer_id INT COMMENT 'Foreign key referencing the customer_id in customers table',
    product_id INT,
    order_date DATE COMMENT 'Date of the order',
    FOREIGN KEY (customer_id) REFERENCES sales_data.customer_info.customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES sales_data.customer_info.products(product_id)
);



---
INSERT INTO sales_data.customer_info.customers (customer_id, first_name, last_name, email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com'),
    (3, 'Alice', 'Johnson', 'alice.johnson@example.com');


---
INSERT INTO sales_data.customer_info.products (product_id, product_name, price)
VALUES
    (101, 'Product A', 29.99),
    (102, 'Product B', 49.99),
    (103, 'Product C', 19.99);

---
INSERT INTO sales_data.customer_info.orders (order_id, customer_id, product_id, order_date)
VALUES
    (1, 1, 101, '2024-05-10'),
    (2, 2, 102, '2024-05-11'),
    (3, 3, 103, '2024-05-12');
