import pandas as pd
from pathlib import Path


# ---------------------------------------
# Project paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DIR = BASE_DIR / "Data" / "cleaned"


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

sellers = pd.read_csv(
    BASE_DIR / "Data" / "raw" / "olist_sellers_dataset.csv"
)


print("=" * 60)
print("REFERENTIAL INTEGRITY VALIDATION")
print("=" * 60)


# ---------------------------------------
# Dataset sizes
# ---------------------------------------

print("\nDataset Shapes:")

print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Products:", products.shape)
print("Sellers:", sellers.shape)


# ---------------------------------------
# 1. Orders -> Customers
# ---------------------------------------

print("\n" + "-" * 60)
print("1. ORDERS -> CUSTOMERS")
print("-" * 60)

invalid_order_customers = orders[
    ~orders["customer_id"].isin(
        customers["customer_id"]
    )
]

print(
    "Orders with missing customer:",
    len(invalid_order_customers)
)


# ---------------------------------------
# 2. Order Items -> Orders
# ---------------------------------------

print("\n" + "-" * 60)
print("2. ORDER ITEMS -> ORDERS")
print("-" * 60)

invalid_order_items = order_items[
    ~order_items["order_id"].isin(
        orders["order_id"]
    )
]

print(
    "Order items with missing order:",
    len(invalid_order_items)
)


# ---------------------------------------
# 3. Order Items -> Products
# ---------------------------------------

print("\n" + "-" * 60)
print("3. ORDER ITEMS -> PRODUCTS")
print("-" * 60)

invalid_products = order_items[
    ~order_items["product_id"].isin(
        products["product_id"]
    )
]

print(
    "Order items with missing product:",
    len(invalid_products)
)


# ---------------------------------------
# 4. Order Items -> Sellers
# ---------------------------------------

print("\n" + "-" * 60)
print("4. ORDER ITEMS -> SELLERS")
print("-" * 60)

invalid_sellers = order_items[
    ~order_items["seller_id"].isin(
        sellers["seller_id"]
    )
]

print(
    "Order items with missing seller:",
    len(invalid_sellers)
)


# ---------------------------------------
# 5. Customers with no orders
# ---------------------------------------

print("\n" + "-" * 60)
print("5. CUSTOMERS WITHOUT ORDERS")
print("-" * 60)

customers_without_orders = customers[
    ~customers["customer_id"].isin(
        orders["customer_id"]
    )
]

print(
    "Customers without orders:",
    len(customers_without_orders)
)


# ---------------------------------------
# 6. Products never ordered
# ---------------------------------------

print("\n" + "-" * 60)
print("6. PRODUCTS NEVER ORDERED")
print("-" * 60)

products_without_orders = products[
    ~products["product_id"].isin(
        order_items["product_id"]
    )
]

print(
    "Products never ordered:",
    len(products_without_orders)
)


# ---------------------------------------
# 7. Orders with multiple items
# ---------------------------------------

print("\n" + "-" * 60)
print("7. ORDERS WITH MULTIPLE ITEMS")
print("-" * 60)

items_per_order = (
    order_items
    .groupby("order_id")
    .size()
)

multiple_item_orders = items_per_order[
    items_per_order > 1
]

print(
    "Orders with multiple items:",
    len(multiple_item_orders)
)

print(
    "Maximum items in one order:",
    items_per_order.max()
)


# ---------------------------------------
# 8. Summary
# ---------------------------------------

print("\n" + "=" * 60)
print("REFERENTIAL INTEGRITY SUMMARY")
print("=" * 60)

print(
    "\nOrders without customers:",
    len(invalid_order_customers)
)

print(
    "Order items without orders:",
    len(invalid_order_items)
)

print(
    "Order items without products:",
    len(invalid_products)
)

print(
    "Order items without sellers:",
    len(invalid_sellers)
)

print(
    "Customers without orders:",
    len(customers_without_orders)
)

print(
    "Products never ordered:",
    len(products_without_orders)
)

print(
    "Orders with multiple items:",
    len(multiple_item_orders)
)

print("\nValidation completed.")