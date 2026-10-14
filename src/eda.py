import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


# ---------------------------------------
# Project paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CLEANED_DIR = BASE_DIR / "Data" / "cleaned"
RAW_DIR = BASE_DIR / "Data" / "raw"

CHART_DIR = BASE_DIR / "outputs" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------
# Load cleaned datasets
# ---------------------------------------

customers = pd.read_csv(
    CLEANED_DIR / "customers_cleaned.csv"
)

orders = pd.read_csv(
    CLEANED_DIR / "orders_cleaned.csv"
)

order_items = pd.read_csv(
    CLEANED_DIR / "order_items_cleaned.csv"
)

products = pd.read_csv(
    CLEANED_DIR / "products_cleaned.csv"
)


# ---------------------------------------
# Load supporting datasets
# ---------------------------------------

payments = pd.read_csv(
    RAW_DIR / "olist_order_payments_dataset.csv"
)

reviews = pd.read_csv(
    RAW_DIR / "olist_order_reviews_dataset.csv"
)

sellers = pd.read_csv(
    RAW_DIR / "olist_sellers_dataset.csv"
)


print("=" * 60)
print("E-COMMERCE EXPLORATORY DATA ANALYSIS")
print("=" * 60)


# ---------------------------------------
# Dataset shapes
# ---------------------------------------

print("\nDataset Shapes:")

print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Products:", products.shape)
print("Payments:", payments.shape)
print("Reviews:", reviews.shape)
print("Sellers:", sellers.shape)

# ---------------------------------------
# Core Business KPIs
# ---------------------------------------

total_orders = orders["order_id"].nunique()

total_customers = customers["customer_unique_id"].nunique()

total_items_sold = order_items["order_item_id"].count()

total_products = products["product_id"].nunique()

total_sellers = sellers["seller_id"].nunique()

gross_item_value = order_items["item_total"].sum()

average_order_value = (
    order_items
    .groupby("order_id")["item_total"]
    .sum()
    .mean()
)

average_item_value = order_items["item_total"].mean()


print("\n" + "=" * 60)
print("CORE BUSINESS KPIs")
print("=" * 60)

print(f"\nTotal Orders: {total_orders:,}")

print(f"Unique Customers: {total_customers:,}")

print(f"Total Items Sold: {total_items_sold:,}")

print(f"Total Products: {total_products:,}")

print(f"Total Sellers: {total_sellers:,}")

print(f"Gross Item Value: ₹{gross_item_value:,.2f}")

print(f"Average Order Value: ₹{average_order_value:,.2f}")

print(f"Average Item Value: ₹{average_item_value:,.2f}")

# ---------------------------------------
# Order Status Analysis
# ---------------------------------------

order_status = (
    orders["order_status"]
    .value_counts()
)

print("\n" + "=" * 60)
print("ORDER STATUS")
print("=" * 60)

print(order_status)

# ---------------------------------------
# Revenue by Order Status
# ---------------------------------------

revenue_by_status = (
    order_items
    .merge(
        orders[["order_id", "order_status"]],
        on="order_id",
        how="left"
    )
    .groupby("order_status")["item_total"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 60)
print("REVENUE BY ORDER STATUS")
print("=" * 60)

print(revenue_by_status)

# ---------------------------------------
# Orders by Year
# ---------------------------------------

orders_by_year = (
    orders
    .groupby("order_year")
    .size()
)

print("\n" + "=" * 60)
print("ORDERS BY YEAR")
print("=" * 60)

print(orders_by_year)

# ---------------------------------------
# Revenue by Year
# ---------------------------------------

revenue_yearly = (
    order_items
    .merge(
        orders[["order_id", "order_year"]],
        on="order_id",
        how="left"
    )
    .groupby("order_year")["item_total"]
    .sum()
)

print("\n" + "=" * 60)
print("REVENUE BY YEAR")
print("=" * 60)

print(revenue_yearly)

# ---------------------------------------
# Monthly Order Analysis
# ---------------------------------------

monthly_orders = (
    orders
    .groupby("order_year_month")
    .size()
)

print("\n" + "=" * 60)
print("MONTHLY ORDERS")
print("=" * 60)

print(monthly_orders)


# ---------------------------------------
# Monthly Revenue Analysis
# ---------------------------------------

orders_with_items = order_items.merge(
    orders[["order_id", "order_year_month"]],
    on="order_id",
    how="left"
)

monthly_revenue = (
    orders_with_items
    .groupby("order_year_month")["item_total"]
    .sum()
)

print("\n" + "=" * 60)
print("MONTHLY REVENUE")
print("=" * 60)

print(monthly_revenue)


# ---------------------------------------
# Highest Order Volume Months
# ---------------------------------------

top_order_months = (
    monthly_orders
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 MONTHS BY ORDER VOLUME")
print("=" * 60)

print(top_order_months)


# ---------------------------------------
# Highest Revenue Months
# ---------------------------------------

top_revenue_months = (
    monthly_revenue
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 MONTHS BY REVENUE")
print("=" * 60)

print(top_revenue_months)

# ---------------------------------------
# Monthly Orders Chart
# ---------------------------------------

monthly_orders_plot = monthly_orders.loc[
    "2017-01":"2018-08"
]

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_orders_plot.index,
    monthly_orders_plot.values,
    marker="o"
)

plt.title("Monthly Order Volume")
plt.xlabel("Month")
plt.ylabel("Number of Orders")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "monthly_orders.png",
    dpi=300
)
# ---------------------------------------
# Monthly Revenue Chart
# ---------------------------------------

monthly_revenue_plot = monthly_revenue.loc[
    "2017-01":"2018-08"
]

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue_plot.index,
    monthly_revenue_plot.values,
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "monthly_revenue.png",
    dpi=300
)

# ---------------------------------------
# Order Status Chart
# ---------------------------------------

plt.figure(figsize=(10, 6))

order_status.sort_values().plot(
    kind="barh"
)

plt.title("Orders by Status")
plt.xlabel("Number of Orders")
plt.ylabel("Order Status")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "order_status.png",
    dpi=300
)

# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER ANALYSIS")
print("=" * 60)


# ---------------------------------------
# Create customer-order dataset
# ---------------------------------------

customer_orders = (
    customers[
        ["customer_id", "customer_unique_id"]
    ]
    .merge(
        orders[
            ["order_id", "customer_id"]
        ],
        on="customer_id",
        how="inner"
    )
)


# ---------------------------------------
# Orders per customer
# ---------------------------------------

orders_per_customer = (
    customer_orders
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)


# ---------------------------------------
# One-time customers
# ---------------------------------------

one_time_customers = (
    orders_per_customer == 1
).sum()


# ---------------------------------------
# Repeat customers
# ---------------------------------------

repeat_customers = (
    orders_per_customer > 1
).sum()


# ---------------------------------------
# Repeat customer rate
# ---------------------------------------

repeat_customer_rate = (
    repeat_customers
    / len(orders_per_customer)
) * 100


print("\nUnique Customers:")
print(len(orders_per_customer))

print("\nOne-time Customers:")
print(one_time_customers)

print("\nRepeat Customers:")
print(repeat_customers)

print(
    f"\nRepeat Customer Rate: "
    f"{repeat_customer_rate:.2f}%"
)


# ---------------------------------------
# Orders per customer statistics
# ---------------------------------------

print("\n" + "-" * 60)
print("ORDERS PER CUSTOMER")
print("-" * 60)

print(
    orders_per_customer.describe()
)

# ---------------------------------------
# Customer Revenue
# ---------------------------------------

customer_revenue = (
    customer_orders
    .merge(
        order_items[
            ["order_id", "item_total"]
        ],
        on="order_id",
        how="left"
    )
    .groupby("customer_unique_id")["item_total"]
    .sum()
)


print("\n" + "-" * 60)
print("CUSTOMER REVENUE")
print("-" * 60)

print(
    customer_revenue.describe()
)


# ---------------------------------------
# Average revenue per customer
# ---------------------------------------

average_customer_revenue = (
    customer_revenue.mean()
)

print(
    f"\nAverage Revenue per Customer: "
    f"₹{average_customer_revenue:,.2f}"
)


# ---------------------------------------
# Top 10 customers
# ---------------------------------------

top_customers = (
    customer_revenue
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "-" * 60)
print("TOP 10 CUSTOMERS BY REVENUE")
print("-" * 60)

print(top_customers)

# ---------------------------------------
# Customer Order Frequency
# ---------------------------------------

order_frequency = (
    orders_per_customer
    .value_counts()
    .sort_index()
)

print("\n" + "-" * 60)
print("CUSTOMER ORDER FREQUENCY")
print("-" * 60)

print(order_frequency)

# ---------------------------------------
# Customer Order Frequency Chart
# ---------------------------------------

plt.figure(figsize=(10, 6))

order_frequency.head(10).plot(
    kind="bar"
)

plt.title("Customer Order Frequency")
plt.xlabel("Number of Orders")
plt.ylabel("Number of Customers")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "customer_order_frequency.png",
    dpi=300
)
# ============================================================
# CUSTOMER REVENUE QUALITY CHECK
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER REVENUE QUALITY CHECK")
print("=" * 60)


# ---------------------------------------
# Customers with zero revenue
# ---------------------------------------

zero_revenue_customers = customer_revenue[
    customer_revenue == 0
]

print(
    "\nCustomers with zero revenue:",
    len(zero_revenue_customers)
)


# ---------------------------------------
# Customers with negative revenue
# ---------------------------------------

negative_revenue_customers = customer_revenue[
    customer_revenue < 0
]

print(
    "Customers with negative revenue:",
    len(negative_revenue_customers)
)


# ---------------------------------------
# Revenue percentiles
# ---------------------------------------

print("\nCustomer Revenue Percentiles:")

print(
    customer_revenue.quantile(
        [0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    )
)


# ---------------------------------------
# High-value customers
# ---------------------------------------

high_value_customers = customer_revenue[
    customer_revenue >= 1000
]

print(
    "\nCustomers with revenue >= ₹1,000:",
    len(high_value_customers)
)

# ============================================================
# PRODUCT & CATEGORY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("PRODUCT & CATEGORY ANALYSIS")
print("=" * 60)


# ---------------------------------------
# Merge order items with products
# ---------------------------------------

product_sales = order_items.merge(
    products[
        [
            "product_id",
            "product_category_name",
            "product_category_name_english"
        ]
    ],
    on="product_id",
    how="left"
)


# ---------------------------------------
# Category units sold
# ---------------------------------------

category_units = (
    product_sales
    .groupby("product_category_name_english")
    ["order_item_id"]
    .count()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 CATEGORIES BY UNITS SOLD")
print("-" * 60)

print(
    category_units.head(10)
)


# ---------------------------------------
# Category revenue
# ---------------------------------------

category_revenue = (
    product_sales
    .groupby("product_category_name_english")
    ["item_total"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 CATEGORIES BY REVENUE")
print("-" * 60)

print(
    category_revenue.head(10)
)


# ---------------------------------------
# Category average item value
# ---------------------------------------

category_average_value = (
    product_sales
    .groupby("product_category_name_english")
    ["item_total"]
    .mean()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 CATEGORIES BY AVERAGE ITEM VALUE")
print("-" * 60)

print(
    category_average_value.head(10)
)


# ---------------------------------------
# Unique products sold
# ---------------------------------------

unique_products_sold = (
    order_items["product_id"]
    .nunique()
)

print("\n" + "-" * 60)
print("PRODUCT COVERAGE")
print("-" * 60)

print(
    "Unique products sold:",
    unique_products_sold
)

print(
    "Products in catalog:",
    products["product_id"].nunique()
)


# ---------------------------------------
# Top products by revenue
# ---------------------------------------

product_revenue = (
    order_items
    .groupby("product_id")["item_total"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 PRODUCTS BY REVENUE")
print("-" * 60)

print(
    product_revenue.head(10)
)


# ---------------------------------------
# Top products by units sold
# ---------------------------------------

product_units = (
    order_items
    .groupby("product_id")
    .size()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 PRODUCTS BY UNITS SOLD")
print("-" * 60)

print(
    product_units.head(10)
)

# ============================================================
# DELIVERED SALES ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("DELIVERED SALES ANALYSIS")
print("=" * 60)


# ---------------------------------------
# Add order status to order items
# ---------------------------------------

items_with_status = order_items.merge(
    orders[
        ["order_id", "order_status"]
    ],
    on="order_id",
    how="left"
)


# ---------------------------------------
# Revenue by status
# ---------------------------------------

status_sales = (
    items_with_status
    .groupby("order_status")["item_total"]
    .agg(
        order_item_value="sum",
        item_count="count"
    )
    .sort_values(
        "order_item_value",
        ascending=False
    )
)

print("\nSales by Order Status:")
print(status_sales)


# ---------------------------------------
# Delivered sales
# ---------------------------------------

delivered_items = items_with_status[
    items_with_status["order_status"] == "delivered"
]

delivered_revenue = delivered_items[
    "item_total"
].sum()

delivered_item_count = len(
    delivered_items
)

delivered_orders = delivered_items[
    "order_id"
].nunique()


print("\nDelivered Revenue:")
print(
    f"₹{delivered_revenue:,.2f}"
)

print("\nDelivered Items:")
print(
    f"{delivered_item_count:,}"
)

print("\nDelivered Orders:")
print(
    f"{delivered_orders:,}"
)


# ---------------------------------------
# Delivered Average Order Value
# ---------------------------------------

delivered_order_values = (
    delivered_items
    .groupby("order_id")["item_total"]
    .sum()
)

delivered_aov = (
    delivered_order_values.mean()
)

print("\nDelivered Average Order Value:")
print(
    f"₹{delivered_aov:,.2f}"
)
# ============================================================
# DELIVERED CATEGORY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("DELIVERED CATEGORY ANALYSIS")
print("=" * 60)


# ---------------------------------------
# Merge delivered items with products
# ---------------------------------------

delivered_product_sales = delivered_items.merge(
    products[
        [
            "product_id",
            "product_category_name",
            "product_category_name_english"
        ]
    ],
    on="product_id",
    how="left"
)


# ---------------------------------------
# Units sold by category
# ---------------------------------------

delivered_category_units = (
    delivered_product_sales
    .groupby("product_category_name_english")
    ["order_item_id"]
    .count()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 CATEGORIES BY DELIVERED UNITS")
print("-" * 60)

print(
    delivered_category_units.head(10)
)


# ---------------------------------------
# Revenue by category
# ---------------------------------------

delivered_category_revenue = (
    delivered_product_sales
    .groupby("product_category_name_english")
    ["item_total"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 CATEGORIES BY DELIVERED REVENUE")
print("-" * 60)

print(
    delivered_category_revenue.head(10)
)


# ---------------------------------------
# Average item value
# ---------------------------------------

delivered_category_average = (
    delivered_product_sales
    .groupby("product_category_name_english")
    ["item_total"]
    .mean()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 CATEGORIES BY DELIVERED AVERAGE ITEM VALUE")
print("-" * 60)

print(
    delivered_category_average.head(10)
)
# ------------------------------------------------------------
# Top 10 categories by delivered units
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

delivered_category_units.head(10).sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Categories by Delivered Units")
plt.xlabel("Delivered Units")
plt.ylabel("Category")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_categories_delivered_units.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Top 10 categories by delivered revenue
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

delivered_category_revenue.head(10).sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Categories by Delivered Revenue")
plt.xlabel("Delivered Revenue")
plt.ylabel("Category")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_categories_delivered_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Top 10 categories by average item value
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

delivered_category_average.head(10).sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Categories by Average Item Value")
plt.xlabel("Average Item Value")
plt.ylabel("Category")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_categories_average_item_value.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nCategory charts saved successfully.")

# ============================================================
# SELLER PERFORMANCE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("SELLER PERFORMANCE ANALYSIS")
print("=" * 60)

# Merge delivered items with seller information
delivered_seller_sales = delivered_items.merge(
    sellers,
    on="seller_id",
    how="left"
)

# ------------------------------------------------------------
# Seller KPIs
# ------------------------------------------------------------

seller_performance = (
    delivered_seller_sales
    .groupby("seller_id")
    .agg(
        delivered_items=("order_item_id", "count"),
        delivered_sales=("item_total", "sum"),
        average_item_value=("item_total", "mean"),
        unique_products=("product_id", "nunique")
    )
    .sort_values("delivered_sales", ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 SELLERS BY DELIVERED SALES")
print("-" * 60)

print(seller_performance.head(10))


# ------------------------------------------------------------
# Top sellers by delivered units
# ------------------------------------------------------------

top_sellers_units = (
    seller_performance
    .sort_values("delivered_items", ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 SELLERS BY DELIVERED UNITS")
print("-" * 60)

print(top_sellers_units.head(10))


# ------------------------------------------------------------
# Top sellers by average item value
# ------------------------------------------------------------

top_sellers_average = (
    seller_performance
    .sort_values("average_item_value", ascending=False)
)

print("\n" + "-" * 60)
print("TOP 10 SELLERS BY AVERAGE ITEM VALUE")
print("-" * 60)

print(top_sellers_average.head(10))


# ------------------------------------------------------------
# Seller summary
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("SELLER SUMMARY")
print("-" * 60)

print("Total sellers:", len(seller_performance))
print(
    "Average delivered sales per seller: ₹",
    round(seller_performance["delivered_sales"].mean(), 2)
)
print(
    "Median delivered sales per seller: ₹",
    round(seller_performance["delivered_sales"].median(), 2)
)

# ============================================================
# SELLER VISUALIZATIONS
# ============================================================

# ------------------------------------------------------------
# Top 10 sellers by delivered sales
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

seller_performance["delivered_sales"].head(10).sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Sellers by Delivered Sales")
plt.xlabel("Delivered Sales")
plt.ylabel("Seller ID")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_sellers_delivered_sales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Top 10 sellers by delivered units
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

seller_performance["delivered_items"].sort_values(
    ascending=False
).head(10).sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Sellers by Delivered Units")
plt.xlabel("Delivered Units")
plt.ylabel("Seller ID")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_sellers_delivered_units.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("\nSeller charts saved successfully.")
# ============================================================
# PAYMENT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("PAYMENT ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# Payment method count
# ------------------------------------------------------------

payment_method_count = (
    payments["payment_type"]
    .value_counts()
)

print("\n" + "-" * 60)
print("PAYMENT METHOD COUNT")
print("-" * 60)

print(payment_method_count)


# ------------------------------------------------------------
# Payment value by method
# ------------------------------------------------------------

payment_value_by_method = (
    payments
    .groupby("payment_type")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("PAYMENT VALUE BY METHOD")
print("-" * 60)

print(payment_value_by_method)


# ------------------------------------------------------------
# Average payment value
# ------------------------------------------------------------

average_payment_by_method = (
    payments
    .groupby("payment_type")["payment_value"]
    .mean()
    .sort_values(ascending=False)
)

print("\n" + "-" * 60)
print("AVERAGE PAYMENT VALUE BY METHOD")
print("-" * 60)

print(average_payment_by_method)


# ------------------------------------------------------------
# Installment distribution
# ------------------------------------------------------------

installment_distribution = (
    payments["payment_installments"]
    .value_counts()
    .sort_index()
)

print("\n" + "-" * 60)
print("PAYMENT INSTALLMENT DISTRIBUTION")
print("-" * 60)

print(installment_distribution)
# ============================================================
# PAYMENT VISUALIZATIONS
# ============================================================

# ------------------------------------------------------------
# Payment method count
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

payment_method_count.sort_values().plot(
    kind="barh"
)

plt.title("Payment Method Distribution")
plt.xlabel("Number of Payments")
plt.ylabel("Payment Method")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "payment_method_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Payment value by method
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

payment_value_by_method.sort_values().plot(
    kind="barh"
)

plt.title("Payment Value by Payment Method")
plt.xlabel("Payment Value")
plt.ylabel("Payment Method")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "payment_value_by_method.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Installment distribution
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

installment_distribution.plot(
    kind="bar"
)

plt.title("Payment Installment Distribution")
plt.xlabel("Number of Installments")
plt.ylabel("Number of Payments")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "payment_installment_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nPayment charts saved successfully.")
# ============================================================
# REVIEW ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("REVIEW ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# Review score distribution
# ------------------------------------------------------------

review_score_count = (
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

print("\n" + "-" * 60)
print("REVIEW SCORE DISTRIBUTION")
print("-" * 60)

print(review_score_count)


# ------------------------------------------------------------
# Average review score
# ------------------------------------------------------------

average_review_score = reviews["review_score"].mean()

print("\n" + "-" * 60)
print("AVERAGE REVIEW SCORE")
print("-" * 60)

print(round(average_review_score, 2))


# ------------------------------------------------------------
# Review scores by order status
# ------------------------------------------------------------

review_status = reviews.merge(
    orders[["order_id", "order_status"]],
    on="order_id",
    how="left"
)

review_score_by_status = (
    review_status
    .groupby("order_status")["review_score"]
    .agg(["count", "mean"])
    .sort_values("mean", ascending=False)
)

print("\n" + "-" * 60)
print("REVIEW SCORE BY ORDER STATUS")
print("-" * 60)

print(review_score_by_status)


# ------------------------------------------------------------
# Review comments
# ------------------------------------------------------------

review_title_missing = reviews["review_comment_title"].isna().sum()
review_message_missing = reviews["review_comment_message"].isna().sum()

print("\n" + "-" * 60)
print("REVIEW COMMENT AVAILABILITY")
print("-" * 60)

print("Missing review titles:", review_title_missing)
print("Missing review messages:", review_message_missing)

print(
    "Review titles available:",
    reviews["review_comment_title"].notna().sum()
)

print(
    "Review messages available:",
    reviews["review_comment_message"].notna().sum()
)
# ============================================================
# REVIEW VISUALIZATIONS
# ============================================================

# ------------------------------------------------------------
# Review score distribution
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

review_score_count.plot(
    kind="bar"
)

plt.title("Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "review_score_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Average review score by order status
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

review_score_by_status["mean"].sort_values().plot(
    kind="barh"
)

plt.title("Average Review Score by Order Status")
plt.xlabel("Average Review Score")
plt.ylabel("Order Status")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "average_review_score_by_status.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nReview charts saved successfully.")
# ============================================================
# DELIVERY PERFORMANCE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("DELIVERY PERFORMANCE ANALYSIS")
print("=" * 60)

# Use only delivered orders with valid delivery dates
delivered_orders = orders[
    (orders["order_status"] == "delivered") &
    (orders["delivery_days"].notna())
].copy()


# ------------------------------------------------------------
# Delivery time summary
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("DELIVERY TIME SUMMARY")
print("-" * 60)

print(
    "Delivered orders:",
    len(delivered_orders)
)

print(
    "Average delivery time:",
    round(delivered_orders["delivery_days"].mean(), 2),
    "days"
)

print(
    "Median delivery time:",
    round(delivered_orders["delivery_days"].median(), 2),
    "days"
)

print(
    "Minimum delivery time:",
    delivered_orders["delivery_days"].min(),
    "days"
)

print(
    "Maximum delivery time:",
    delivered_orders["delivery_days"].max(),
    "days"
)


# ------------------------------------------------------------
# Estimated vs actual delivery
# ------------------------------------------------------------

print("\n" + "-" * 60)
print("DELIVERY DELAY ANALYSIS")
print("-" * 60)

print(
    "Average estimated delivery time:",
    round(
        delivered_orders["estimated_delivery_days"].mean(),
        2
    ),
    "days"
)

print(
    "Average delivery delay:",
    round(
        delivered_orders["delivery_delay_days"].mean(),
        2
    ),
    "days"
)

print(
    "Orders delivered early/on time:",
    (
        delivered_orders["delivery_delay_days"] <= 0
    ).sum()
)

print(
    "Orders delivered late:",
    (
        delivered_orders["delivery_delay_days"] > 0
    ).sum()
)


# ------------------------------------------------------------
# Delivery time by year
# ------------------------------------------------------------

delivery_by_year = (
    delivered_orders
    .groupby("order_year")["delivery_days"]
    .agg(["count", "mean", "median"])
)

print("\n" + "-" * 60)
print("DELIVERY TIME BY YEAR")
print("-" * 60)

print(delivery_by_year)


# ------------------------------------------------------------
# Delivery delay by year
# ------------------------------------------------------------

delay_by_year = (
    delivered_orders
    .groupby("order_year")["delivery_delay_days"]
    .mean()
)

print("\n" + "-" * 60)
print("AVERAGE DELIVERY DELAY BY YEAR")
print("-" * 60)

print(delay_by_year)
# ============================================================
# DELIVERY VISUALIZATIONS
# ============================================================

# ------------------------------------------------------------
# Delivery time distribution
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

delivered_orders["delivery_days"].plot(
    kind="hist",
    bins=30
)

plt.title("Delivery Time Distribution")
plt.xlabel("Delivery Time (Days)")
plt.ylabel("Number of Orders")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "delivery_time_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Average delivery time by year
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

delivery_by_year["mean"].plot(
    kind="bar"
)

plt.title("Average Delivery Time by Year")
plt.xlabel("Year")
plt.ylabel("Average Delivery Time (Days)")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "average_delivery_time_by_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Average delivery delay by year
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

delay_by_year.plot(
    kind="bar"
)

plt.title("Average Delivery Delay by Year")
plt.xlabel("Year")
plt.ylabel("Average Delay (Days)")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "average_delivery_delay_by_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nDelivery charts saved successfully.")