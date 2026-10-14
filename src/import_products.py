import pandas as pd
import mysql.connector

csv_path = r"C:\Users\acer\OneDrive\Desktop\Projects\Ecom\Data\cleaned\products_cleaned.csv"

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
INSERT INTO products (
    product_id,
    product_category_name,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm,
    product_category_name_english
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

records = df.values.tolist()

batch_size = 5000

for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    cursor.executemany(query, batch)
    conn.commit()
    print(f"Imported {min(i + batch_size, len(records))} / {len(records)} rows")

cursor.close()
conn.close()

print("Products import completed.")