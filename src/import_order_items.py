import pandas as pd
import mysql.connector

csv_path = r"C:\Users\acer\OneDrive\Desktop\Projects\Ecom\Data\cleaned\order_items_cleaned.csv"

# Read CSV
df = pd.read_csv(csv_path)

# Convert NaN to None
df = df.astype(object).where(pd.notna(df), None)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="ecommerce_db"
)

cursor = conn.cursor()

query = """
INSERT INTO order_items (
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value,
    item_total
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

records = df.values.tolist()

batch_size = 5000

for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    cursor.executemany(query, batch)
    conn.commit()

    print(
        f"Imported {min(i + batch_size, len(records))} / {len(records)} rows"
    )

cursor.close()
conn.close()

print("Order items import completed.")