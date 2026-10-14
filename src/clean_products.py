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

input_file = RAW_DIR / "olist_products_dataset.csv"
output_file = CLEANED_DIR / "products_cleaned.csv"


# ---------------------------------------
# Load dataset
# ---------------------------------------

df = pd.read_csv(input_file)

print("=" * 60)
print("PRODUCT DATA CLEANING")
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
# 2. Fix Olist spelling mistakes
# ---------------------------------------

df = df.rename(columns={
    "product_name_lenght": "product_name_length",
    "product_description_lenght": "product_description_length"
})

print("\nCorrected Column Names:")
print(df.columns.tolist())


# ---------------------------------------
# 3. Missing values
# ---------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())


# ---------------------------------------
# 4. Duplicate rows
# ---------------------------------------

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ---------------------------------------
# 5. Duplicate Product IDs
# ---------------------------------------

duplicate_product_ids = (
    df["product_id"].duplicated().sum()
)

print("\nDuplicate Product IDs:")
print(duplicate_product_ids)


# ---------------------------------------
# 6. Check product categories
# ---------------------------------------

print("\nUnique Product Categories:")
print(df["product_category_name"].nunique())

print("\nMissing Product Categories:")
print(
    df["product_category_name"].isnull().sum()
)


# ---------------------------------------
# 7. Check numerical columns
# ---------------------------------------

numeric_columns = [
    "product_name_length",
    "product_description_length",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

print("\nNegative Values:")

for column in numeric_columns:

    negative_count = (
        df[column] < 0
    ).sum()

    print(
        f"{column}: {negative_count}"
    )


# ---------------------------------------
# 8. Check zero values
# ---------------------------------------

print("\nZero Values:")

for column in numeric_columns:

    zero_count = (
        df[column] == 0
    ).sum()

    print(
        f"{column}: {zero_count}"
    )


# ---------------------------------------
# 9. Investigate rows with missing values
# ---------------------------------------

missing_product_data = df[
    df.isnull().any(axis=1)
]

print("\nRows With Missing Values:")
print(len(missing_product_data))

print("\nMissing Data Pattern:")

print(
    missing_product_data.isnull().sum()
)


# ---------------------------------------
# 10. Investigate the two dimension records
# ---------------------------------------

missing_dimensions = df[
    df[
        [
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    ].isnull().any(axis=1)
]

print("\nProducts With Missing Dimensions:")
print(missing_dimensions)

# ---------------------------------------
# 10A. Check whether incomplete products
#     appear in order items
# ---------------------------------------

order_items_file = RAW_DIR / "olist_order_items_dataset.csv"

order_items = pd.read_csv(
    order_items_file,
    usecols=["product_id"]
)

sold_product_ids = set(
    order_items["product_id"].unique()
)

incomplete_products = df[
    df["product_category_name"].isnull()
]

# ---------------------------------------
# 10B. Investigate zero-weight products
# ---------------------------------------

zero_weight_products = df[
    df["product_weight_g"] == 0
]

print("\nProducts With Zero Weight:")
print(zero_weight_products[
    [
        "product_id",
        "product_category_name",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]
])
# ---------------------------------------
# 11. Standardize category text
# ---------------------------------------

df["product_category_name"] = (
    df["product_category_name"]
    .str.strip()
    .str.lower()
)
# ---------------------------------------
# 11A. Translate product categories
# ---------------------------------------

translation_file = (
    RAW_DIR / "product_category_name_translation.csv"
)

translation_df = pd.read_csv(
    translation_file
)

translation_df["product_category_name"] = (
    translation_df["product_category_name"]
    .str.strip()
    .str.lower()
)

translation_df["product_category_name_english"] = (
    translation_df["product_category_name_english"]
    .str.strip()
    .str.lower()
)


df = df.merge(
    translation_df,
    on="product_category_name",
    how="left"
)
print("\nCategory Translation Missing Values:")

print(
    df["product_category_name_english"]
    .isnull()
    .sum()
)
print("\nTranslated Categories:")
print(
    df[
        [
            "product_category_name",
            "product_category_name_english"
        ]
    ]
    .drop_duplicates()
    .head(20)
)
# ---------------------------------------
# 11B. Find untranslated categories
# ---------------------------------------

untranslated_categories = df[
    df["product_category_name"].notna()
    &
    df["product_category_name_english"].isna()
]["product_category_name"].unique()

print("\nUntranslated Product Categories:")
print(untranslated_categories)

print(
    "\nNumber of Untranslated Categories:",
    len(untranslated_categories)
)

# ---------------------------------------
# 12. Final validation
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

print("\nDuplicate Product IDs:")
print(
    df["product_id"].duplicated().sum()
)

print("\nSample Data:")
print(df.head())


# ---------------------------------------
# 13. Create cleaned directory
# ---------------------------------------

CLEANED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------
# 14. Save cleaned dataset
# ---------------------------------------

df.to_csv(
    output_file,
    index=False
)

print("\nCleaned product dataset saved to:")
print(output_file)