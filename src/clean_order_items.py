import pandas as pd
from pathlib import Path


# ---------------------------------------
# Project paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "Data" / "raw"
CLEANED_DIR = BASE_DIR / "Data" / "cleaned"


# ---------------------------------------
# File paths
# ---------------------------------------

input_file = RAW_DIR / "olist_order_items_dataset.csv"
output_file = CLEANED_DIR / "order_items_cleaned.csv"


# ---------------------------------------
# Load dataset
# ---------------------------------------

df = pd.read_csv(input_file)

print("=" * 60)
print("ORDER ITEMS DATA CLEANING")
print("=" * 60)

print("\nOriginal Shape:")
print(df.shape)


# ---------------------------------------
# 1. Standardize column names
# ---------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nColumn Names:")
print(df.columns.tolist())


# ---------------------------------------
# 2. Missing values
# ---------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())


# ---------------------------------------
# 3. Duplicate rows
# ---------------------------------------

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ---------------------------------------
# 4. Duplicate Order + Item combinations
# ---------------------------------------

duplicate_order_items = df.duplicated(
    subset=["order_id", "order_item_id"]
).sum()

print("\nDuplicate Order + Item IDs:")
print(duplicate_order_items)


# ---------------------------------------
# 5. Convert date column
# ---------------------------------------

df["shipping_limit_date"] = pd.to_datetime(
    df["shipping_limit_date"],
    errors="coerce"
)

print("\nInvalid Shipping Dates:")
print(
    df["shipping_limit_date"].isnull().sum()
)


# ---------------------------------------
# 6. Validate price
# ---------------------------------------

negative_price = (
    df["price"] < 0
).sum()

print("\nNegative Price Records:")
print(negative_price)


# ---------------------------------------
# 7. Validate freight value
# ---------------------------------------

negative_freight = (
    df["freight_value"] < 0
).sum()

print("\nNegative Freight Records:")
print(negative_freight)


# ---------------------------------------
# 8. Check zero prices
# ---------------------------------------

zero_price = (
    df["price"] == 0
).sum()

print("\nZero Price Records:")
print(zero_price)


# ---------------------------------------
# 9. Create item total
# ---------------------------------------

df["item_total"] = (
    df["price"] +
    df["freight_value"]
)

# ---------------------------------------
# 11. Final validation
# ---------------------------------------

print("\n" + "=" * 60)
print("FINAL VALIDATION")
print("=" * 60)

print("\nFinal Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

print("\nSample Data:")
print(df.head())


# ---------------------------------------
# 12. Create cleaned directory
# ---------------------------------------

CLEANED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------
# 13. Save cleaned dataset
# ---------------------------------------

df.to_csv(
    output_file,
    index=False
)

print("\nCleaned order items dataset saved to:")
print(output_file)