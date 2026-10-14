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

input_file = RAW_DIR / "olist_orders_dataset.csv"
output_file = CLEANED_DIR / "orders_cleaned.csv"


# ---------------------------------------
# Load dataset
# ---------------------------------------

df = pd.read_csv(input_file)

print("=" * 60)
print("ORDER DATA CLEANING")
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
# 4. Check duplicate Order IDs
# ---------------------------------------

duplicate_order_ids = df["order_id"].duplicated().sum()

print("\nDuplicate Order IDs:")
print(duplicate_order_ids)


# ---------------------------------------
# 5. Check duplicate Customer IDs
# ---------------------------------------

duplicate_customer_ids = df["customer_id"].duplicated().sum()

print("\nDuplicate Customer IDs:")
print(duplicate_customer_ids)


# ---------------------------------------
# 6. Check Order Status
# ---------------------------------------

print("\nOrder Status Values:")
print(df["order_status"].value_counts())


# ---------------------------------------
# 7. Convert date columns
# ---------------------------------------

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:

    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )


# ---------------------------------------
# 8. Check invalid dates
# ---------------------------------------

print("\nInvalid/Missing Dates After Conversion:")

for column in date_columns:

    print(
        f"{column}: "
        f"{df[column].isnull().sum()}"
    )


# ---------------------------------------
# 9. Validate purchase → approval
# ---------------------------------------

invalid_approval = df[
    df["order_approved_at"].notna()
    &
    (
        df["order_approved_at"]
        < df["order_purchase_timestamp"]
    )
]

print("\nApproval Before Purchase:")
print(len(invalid_approval))


# ---------------------------------------
# 10. Validate approval → carrier
# ---------------------------------------

invalid_carrier = df[
    df["order_delivered_carrier_date"].notna()
    &
    df["order_approved_at"].notna()
    &
    (
        df["order_delivered_carrier_date"]
        < df["order_approved_at"]
    )
]

print("\nCarrier Date Before Approval:")
print(len(invalid_carrier))


# ---------------------------------------
# 11. Validate carrier → customer delivery
# ---------------------------------------

invalid_delivery = df[
    df["order_delivered_customer_date"].notna()
    &
    df["order_delivered_carrier_date"].notna()
    &
    (
        df["order_delivered_customer_date"]
        < df["order_delivered_carrier_date"]
    )
]

print("\nCustomer Delivery Before Carrier Date:")
print(len(invalid_delivery))


# ---------------------------------------
# 12. Validate estimated delivery
# ---------------------------------------

invalid_estimated = df[
    df["order_delivered_customer_date"].notna()
    &
    (
        df["order_delivered_customer_date"]
        < df["order_purchase_timestamp"]
    )
]

print("\nCustomer Delivery Before Purchase:")
print(len(invalid_estimated))
# ---------------------------------------
# 12A. Investigate invalid date sequences
# ---------------------------------------

print("\n" + "=" * 60)
print("INVESTIGATION OF DATE ISSUES")
print("=" * 60)


# Orders where carrier date is before approval
carrier_before_approval = df[
    df["order_delivered_carrier_date"].notna()
    &
    df["order_approved_at"].notna()
    &
    (
        df["order_delivered_carrier_date"]
        < df["order_approved_at"]
    )
]

print("\nCarrier Before Approval - By Order Status:")
print(
    carrier_before_approval["order_status"]
    .value_counts()
)


# Orders where customer delivery is before carrier date
delivery_before_carrier = df[
    df["order_delivered_customer_date"].notna()
    &
    df["order_delivered_carrier_date"].notna()
    &
    (
        df["order_delivered_customer_date"]
        < df["order_delivered_carrier_date"]
    )
]

print("\nCustomer Delivery Before Carrier - By Order Status:")
print(
    delivery_before_carrier["order_status"]
    .value_counts()
)


# Display sample problematic records
print("\nSample Carrier-Before-Approval Records:")
print(
    carrier_before_approval[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date"
        ]
    ].head(10)
)


print("\nSample Delivery-Before-Carrier Records:")
print(
    delivery_before_carrier[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ]
    ].head(10)
)
# ---------------------------------------
# 12B. Create data quality flags
# ---------------------------------------

df["carrier_before_approval_flag"] = (
    df["order_delivered_carrier_date"].notna()
    &
    df["order_approved_at"].notna()
    &
    (
        df["order_delivered_carrier_date"]
        < df["order_approved_at"]
    )
)


df["delivery_before_carrier_flag"] = (
    df["order_delivered_customer_date"].notna()
    &
    df["order_delivered_carrier_date"].notna()
    &
    (
        df["order_delivered_customer_date"]
        < df["order_delivered_carrier_date"]
    )
)


df["date_quality_issue"] = (
    df["carrier_before_approval_flag"]
    |
    df["delivery_before_carrier_flag"]
)

# ---------------------------------------
# 13. Create delivery metrics
# ---------------------------------------

df["delivery_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.days


df["estimated_delivery_days"] = (
    df["order_estimated_delivery_date"]
    - df["order_purchase_timestamp"]
).dt.days


# ---------------------------------------
# 14. Delivery performance
# ---------------------------------------

df["delivery_delay_days"] = (
    df["order_delivered_customer_date"]
    - df["order_estimated_delivery_date"]
).dt.days


# ---------------------------------------
# 15. Create date features
# ---------------------------------------

df["order_year"] = (
    df["order_purchase_timestamp"].dt.year
)

df["order_month"] = (
    df["order_purchase_timestamp"].dt.month
)

df["order_month_name"] = (
    df["order_purchase_timestamp"].dt.month_name()
)

df["order_quarter"] = (
    df["order_purchase_timestamp"].dt.quarter
)

df["order_year_month"] = (
    df["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)


# ---------------------------------------
# 16. Final validation
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

print("\nOrder Status:")
print(df["order_status"].value_counts())

print("\nSample Data:")
print(df.head())


# ---------------------------------------
# 17. Create cleaned directory
# ---------------------------------------

CLEANED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------
# 18. Save cleaned dataset
# ---------------------------------------

df.to_csv(
    output_file,
    index=False
)

print("\nCleaned order dataset saved to:")
print(output_file)

print("\nData Quality Flags:")

print(
    "Carrier before approval:",
    df["carrier_before_approval_flag"].sum()
)

print(
    "Delivery before carrier:",
    df["delivery_before_carrier_flag"].sum()
)

print(
    "Total date quality issues:",
    df["date_quality_issue"].sum()
)
print("\nDate Quality Issues by Order Status:")

print(
    df.groupby("order_status")["date_quality_issue"]
    .sum()
    .sort_values(ascending=False)
)