import pandas as pd
import mysql.connector

# File path
csv_path = r"C:\Users\acer\OneDrive\Desktop\Projects\Ecom\Data\cleaned\orders_cleaned.csv"

df = pd.read_csv(csv_path)

# Convert pandas NaN values to Python None
df = df.astype(object).where(pd.notna(df), None)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="ecommerce_db"
)

cursor = conn.cursor()

# Insert query
query = """
INSERT INTO orders_staging (
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
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

# Convert DataFrame to records
records = df.values.tolist()

# Insert in batches
batch_size = 5000

for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    cursor.executemany(query, batch)
    conn.commit()
    print(f"Imported {min(i + batch_size, len(records))} / {len(records)} rows")

cursor.close()
conn.close()

print("Orders staging import completed.")