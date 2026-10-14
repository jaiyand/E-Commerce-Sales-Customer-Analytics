import pandas as pd
from pathlib import Path


# ---------------------------------------
# Project paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "Data" / "raw"
CLEANED_DIR = BASE_DIR / "Data" / "cleaned"


# ---------------------------------------
# Load datasets
# ---------------------------------------

orders = pd.read_csv(
    CLEANED_DIR / "orders_cleaned.csv"
)

order_items = pd.read_csv(
    CLEANED_DIR / "order_items_cleaned.csv"
)

products = pd.read_csv(
    CLEANED_DIR / "products_cleaned.csv"
)

payments = pd.read_csv(
    RAW_DIR / "olist_order_payments_dataset.csv"
)

reviews = pd.read_csv(
    RAW_DIR / "olist_order_reviews_dataset.csv"
)

sellers = pd.read_csv(
    RAW_DIR / "olist_sellers_dataset.csv"
)

geolocation = pd.read_csv(
    RAW_DIR / "olist_geolocation_dataset.csv"
)

translation = pd.read_csv(
    RAW_DIR / "product_category_name_translation.csv"
)


print("=" * 60)
print("SUPPORTING DATA VALIDATION")
print("=" * 60)


# ============================================================
# 1. PAYMENTS
# ============================================================

print("\n" + "-" * 60)
print("1. ORDER PAYMENTS")
print("-" * 60)

print("\nShape:")
print(payments.shape)

print("\nMissing Values:")
print(payments.isna().sum())

print("\nDuplicate Rows:")
print(payments.duplicated().sum())

print("\nPayment Types:")
print(payments["payment_type"].value_counts())

print("\nPayment Installments:")
print(payments["payment_installments"].value_counts().sort_index())

print("\nNegative Payment Values:")
print(
    (payments["payment_value"] < 0).sum()
)

print("\nZero Payment Values:")
print(
    (payments["payment_value"] == 0).sum()
)

# Payments -> Orders
invalid_payment_orders = payments[
    ~payments["order_id"].isin(
        orders["order_id"]
    )
]

print(
    "\nPayments with missing order:",
    len(invalid_payment_orders)
)


# ============================================================
# 2. REVIEWS
# ============================================================

print("\n" + "-" * 60)
print("2. ORDER REVIEWS")
print("-" * 60)

print("\nShape:")
print(reviews.shape)

print("\nMissing Values:")
print(reviews.isna().sum())

print("\nDuplicate Rows:")
print(reviews.duplicated().sum())

print("\nReview Scores:")
print(
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

print("\nInvalid Review Scores:")
print(
    (
        (reviews["review_score"] < 1)
        |
        (reviews["review_score"] > 5)
    ).sum()
)

# Reviews -> Orders
invalid_review_orders = reviews[
    ~reviews["order_id"].isin(
        orders["order_id"]
    )
]

print(
    "\nReviews with missing order:",
    len(invalid_review_orders)
)


# ============================================================
# 3. SELLERS
# ============================================================

print("\n" + "-" * 60)
print("3. SELLERS")
print("-" * 60)

print("\nShape:")
print(sellers.shape)

print("\nMissing Values:")
print(sellers.isna().sum())

print("\nDuplicate Rows:")
print(sellers.duplicated().sum())

print("\nDuplicate Seller IDs:")
print(
    sellers["seller_id"].duplicated().sum()
)

# Sellers -> Order Items
unused_sellers = sellers[
    ~sellers["seller_id"].isin(
        order_items["seller_id"]
    )
]

print(
    "\nSellers with no order items:",
    len(unused_sellers)
)


# ============================================================
# 4. GEOLOCATION
# ============================================================

print("\n" + "-" * 60)
print("4. GEOLOCATION")
print("-" * 60)

print("\nShape:")
print(geolocation.shape)

print("\nMissing Values:")
print(geolocation.isna().sum())

print("\nDuplicate Rows:")
print(geolocation.duplicated().sum())

print(
    "\nUnique ZIP Prefixes:",
    geolocation["geolocation_zip_code_prefix"].nunique()
)

print(
    "Unique Cities:",
    geolocation["geolocation_city"].nunique()
)

print(
    "Unique States:",
    geolocation["geolocation_state"].nunique()
)

print("\nInvalid Latitude:")
print(
    (
        (geolocation["geolocation_lat"] < -90)
        |
        (geolocation["geolocation_lat"] > 90)
    ).sum()
)

print("\nInvalid Longitude:")
print(
    (
        (geolocation["geolocation_lng"] < -180)
        |
        (geolocation["geolocation_lng"] > 180)
    ).sum()
)


# ============================================================
# 5. CATEGORY TRANSLATION
# ============================================================

print("\n" + "-" * 60)
print("5. CATEGORY TRANSLATION")
print("-" * 60)

print("\nShape:")
print(translation.shape)

print("\nMissing Values:")
print(translation.isna().sum())

print("\nDuplicate Rows:")
print(translation.duplicated().sum())

print("\nDuplicate Portuguese Categories:")
print(
    translation["product_category_name"]
    .duplicated()
    .sum()
)

print("\nDuplicate English Categories:")
print(
    translation["product_category_name_english"]
    .duplicated()
    .sum()
)


# ============================================================
# 6. SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("SUPPORTING DATA VALIDATION SUMMARY")
print("=" * 60)

print("\nPayments -> Orders:")
print(
    "Invalid references:",
    len(invalid_payment_orders)
)

print("\nReviews -> Orders:")
print(
    "Invalid references:",
    len(invalid_review_orders)
)

print("\nSellers without order items:")
print(
    len(unused_sellers)
)

print("\nGeolocation duplicate rows:")
print(
    geolocation.duplicated().sum()
)

print("\nCategory translation duplicate rows:")
print(
    translation.duplicated().sum()
)

print("\nValidation completed.")