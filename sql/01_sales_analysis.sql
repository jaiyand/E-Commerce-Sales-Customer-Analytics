CREATE DATABASE ecommerce_db;
USE ecommerce_db;
SELECT DATABASE();
CREATE TABLE customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_unique_id VARCHAR(32) NOT NULL,
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state CHAR(2)
);
CREATE TABLE orders (
    order_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32) NOT NULL,
    order_status VARCHAR(20),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE products (
    product_id VARCHAR(32) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g DECIMAL(10,2),
    product_length_cm DECIMAL(10,2),
    product_height_cm DECIMAL(10,2),
    product_width_cm DECIMAL(10,2),
    product_category_name_english VARCHAR(100)
);

CREATE TABLE order_items (
    order_id VARCHAR(32) NOT NULL,
    order_item_id INT NOT NULL,
    product_id VARCHAR(32) NOT NULL,
    seller_id VARCHAR(32),
    shipping_limit_date DATETIME,
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),
    item_total DECIMAL(10,2),

    PRIMARY KEY (order_id, order_item_id),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

ALTER TABLE orders
ADD COLUMN carrier_before_approval_flag TINYINT,
ADD COLUMN delivery_before_carrier_flag TINYINT,
ADD COLUMN date_quality_issue TINYINT,
ADD COLUMN delivery_days DECIMAL(10,2),
ADD COLUMN estimated_delivery_days DECIMAL(10,2),
ADD COLUMN delivery_delay_days DECIMAL(10,2),
ADD COLUMN order_year INT,
ADD COLUMN order_month INT,
ADD COLUMN order_month_name VARCHAR(20),
ADD COLUMN order_quarter VARCHAR(10),
ADD COLUMN order_year_month VARCHAR(10);
ALTER TABLE orders
MODIFY carrier_before_approval_flag VARCHAR(5),
MODIFY delivery_before_carrier_flag VARCHAR(5),
MODIFY date_quality_issue VARCHAR(5);
SHOW TABLES;
DESCRIBE customers;
DESCRIBE orders;
DESCRIBE products;
DESCRIBE order_items;

INSERT INTO orders (
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    carrier_before_approval_flag,
    delivery_before_carrier_flag,
    date_quality_issue,
    delivery_days,
    estimated_delivery_days,
    delivery_delay_days,
    order_year,
    order_month,
    order_month_name,
    order_quarter,
    order_year_month
)
SELECT
    order_id,
    customer_id,
    order_status,

    STR_TO_DATE(NULLIF(order_purchase_timestamp, ''), '%Y-%m-%d %H:%i:%s'),
    STR_TO_DATE(NULLIF(order_approved_at, ''), '%Y-%m-%d %H:%i:%s'),
    STR_TO_DATE(NULLIF(order_delivered_carrier_date, ''), '%Y-%m-%d %H:%i:%s'),
    STR_TO_DATE(NULLIF(order_delivered_customer_date, ''), '%Y-%m-%d %H:%i:%s'),
    STR_TO_DATE(NULLIF(order_estimated_delivery_date, ''), '%Y-%m-%d'),

    carrier_before_approval_flag,
    delivery_before_carrier_flag,
    date_quality_issue,

    CAST(NULLIF(delivery_days, '') AS DECIMAL(10,2)),
    CAST(NULLIF(estimated_delivery_days, '') AS DECIMAL(10,2)),
    CAST(NULLIF(delivery_delay_days, '') AS DECIMAL(10,2)),

    CAST(NULLIF(order_year, '') AS UNSIGNED),
    CAST(NULLIF(order_month, '') AS UNSIGNED),

    order_month_name,
    order_quarter,
    order_year_month

FROM orders_staging;

USE ecommerce_db;
-- =====================================================
-- E-COMMERCE SALES & CUSTOMER ANALYTICS
-- SQL BUSINESS ANALYSIS
-- =====================================================

-- 1. CORE BUSINESS KPIs

SELECT COUNT(*) AS total_orders
FROM orders;

SELECT COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers;

SELECT COUNT(*) AS total_products
FROM products;

SELECT COUNT(*) AS total_order_items
FROM order_items;

SELECT ROUND(SUM(item_total), 2) AS gross_item_value
FROM order_items;

SELECT ROUND(AVG(order_total), 2) AS average_order_value
FROM (
    SELECT order_id, SUM(item_total) AS order_total
    FROM order_items
    GROUP BY order_id
) AS order_values;


-- 2. ORDER STATUS ANALYSIS

SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2)
        AS percentage
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- 3. MONTHLY ORDER TRENDS

SELECT
    order_year,
    order_month,
    order_month_name,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_year, order_month, order_month_name
ORDER BY order_year, order_month;


-- 4. MONTHLY GROSS ITEM VALUE

SELECT
    o.order_year,
    o.order_month,
    o.order_month_name,
    ROUND(SUM(oi.item_total), 2) AS monthly_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.order_year, o.order_month, o.order_month_name
ORDER BY o.order_year, o.order_month;


-- 5. TOP 10 PRODUCT CATEGORIES BY GROSS ITEM VALUE

SELECT
    p.product_category_name_english AS category,
    ROUND(SUM(oi.item_total), 2) AS total_revenue,
    COUNT(*) AS items_sold
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;


-- 6. CUSTOMER STATE ANALYSIS

SELECT
    customer_state,
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM customers
GROUP BY customer_state
ORDER BY total_customers DESC;


-- 7. TOP 10 CUSTOMERS BY GROSS ITEM VALUE

SELECT
    c.customer_unique_id,
    ROUND(SUM(oi.item_total), 2) AS total_spending,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_unique_id
ORDER BY total_spending DESC
LIMIT 10;


-- 8. SELLER PERFORMANCE

SELECT
    seller_id,
    ROUND(SUM(price), 2) AS total_sales,
    COUNT(*) AS items_sold,
    ROUND(AVG(price), 2) AS average_item_price
FROM order_items
GROUP BY seller_id
ORDER BY total_sales DESC
LIMIT 10;


-- 9. DELIVERY PERFORMANCE

SELECT
    COUNT(*) AS delivered_orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delivery_delay_days), 2) AS avg_delay_days,
    SUM(delivery_delay_days > 0) AS delayed_orders
FROM orders
WHERE order_status = 'delivered';


-- 10. DATA INTEGRITY: ORDER REFERENCES

SELECT COUNT(*) AS invalid_order_references
FROM order_items oi
LEFT JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;


-- 11. DATA INTEGRITY: PRODUCT REFERENCES

SELECT COUNT(*) AS invalid_product_references
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;

USE ecommerce_db;
SELECT
    (SELECT COUNT(*) FROM orders) AS total_orders,
    (SELECT COUNT(DISTINCT customer_unique_id)
     FROM customers) AS unique_customers,
    (SELECT COUNT(*) FROM products) AS total_products,
    (SELECT COUNT(*) FROM order_items) AS total_order_items,
    (SELECT ROUND(SUM(item_total), 2)
     FROM order_items) AS gross_item_value;