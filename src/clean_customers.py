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

input_file = RAW_DIR / "olist_customers_dataset.csv"
output_file = CLEANED_DIR / "customers_cleaned.csv"


# ---------------------------------------
# Load dataset
# ---------------------------------------

df = pd.read_csv(input_file)

print("=" * 60)
print("CUSTOMER DATA CLEANING")
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
# 2. Check missing values
# ---------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())


# ---------------------------------------
# 3. Check duplicate rows
# ---------------------------------------

duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows:")
print(duplicate_rows)


# ---------------------------------------
# 4. Check duplicate customer IDs
# ---------------------------------------

duplicate_customer_ids = df["customer_id"].duplicated().sum()

print("\nDuplicate Customer IDs:")
print(duplicate_customer_ids)


# ---------------------------------------
# 5. Check duplicate unique customer IDs
# ---------------------------------------

duplicate_unique_ids = df["customer_unique_id"].duplicated().sum()

print("\nDuplicate Customer Unique IDs:")
print(duplicate_unique_ids)


# ---------------------------------------
# 6. Clean city names
# ---------------------------------------

df["customer_city"] = (
    df["customer_city"]
    .str.strip()
    .str.lower()
)


# ---------------------------------------
# 7. Clean state values
# ---------------------------------------

df["customer_state"] = (
    df["customer_state"]
    .str.strip()
    .str.upper()
)


# ---------------------------------------
# 8. Validate ZIP code
# ---------------------------------------

invalid_zip = df[
    (df["customer_zip_code_prefix"] < 0)
]

print("\nInvalid ZIP Code Records:")
print(len(invalid_zip))


# ---------------------------------------
# 9. Validate customer IDs
# ---------------------------------------

missing_customer_id = df["customer_id"].isnull().sum()

print("\nMissing Customer IDs:")
print(missing_customer_id)


# ---------------------------------------
# 10. Final validation
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

print("\nSample Data:")
print(df.head())


# ---------------------------------------
# 11. Create cleaned directory
# ---------------------------------------

CLEANED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------
# 12. Save cleaned dataset
# ---------------------------------------

df.to_csv(
    output_file,
    index=False
)

print("\nCleaned customer dataset saved to:")
print(output_file)