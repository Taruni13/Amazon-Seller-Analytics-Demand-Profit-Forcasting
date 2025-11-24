#!/usr/bin/env python3
"""
Generate synthetic Amazon sales data similar to `data/amazon_sales_data 2025.csv`.

Produces a CSV with columns:
Order ID,Date,Product,Category,Price,Quantity,Total Sales,Customer Name,Customer Location,Payment Method,Status

Usage:
    python scripts/generate_synthetic_data.py --rows 5000 --output data/amazon_sales_data_2025_synthetic.csv
"""

import csv
import random
import argparse
from datetime import datetime, timedelta

PRODUCTS = [
    ("Running Shoes", "Footwear", 60),
    ("Headphones", "Electronics", 100),
    ("Smartwatch", "Electronics", 150),
    ("Smartphone", "Electronics", 500),
    ("T-Shirt", "Clothing", 20),
    ("Jeans", "Clothing", 40),
    ("Laptop", "Electronics", 800),
    ("Washing Machine", "Home Appliances", 600),
    ("Refrigerator", "Home Appliances", 1200),
    ("Book", "Books", 15),
]

CUSTOMER_FIRST = ["Emma", "Emily", "John", "Olivia", "Michael", "Daniel", "Sophia", "Jane", "David", "Chris", "Daniel", "Daniel", "Alex","Mia","Liam","Noah","Ava","Ethan","Isabella","Lucas"]
CUSTOMER_LAST = ["Clark", "Johnson", "Doe", "Wilson", "Brown", "Harris", "Miller", "Smith", "Lee", "White", "Garcia", "Martinez", "Anderson", "Taylor"]
LOCATIONS = ["New York", "San Francisco", "Denver", "Dallas", "Houston", "Miami", "Boston", "Seattle", "Chicago", "Los Angeles"]
PAYMENT_METHODS = ["Debit Card", "Credit Card", "PayPal", "Amazon Pay", "Gift Card"]
STATUS = ["Completed", "Pending", "Cancelled"]


def random_date(start_date, end_date):
    """Return a random date between start_date and end_date (inclusive).
    Format returned as dd-mm-yy (two-digit year) to match example file.
    """
    delta = end_date - start_date
    rand_days = random.randint(0, delta.days)
    d = start_date + timedelta(days=rand_days)
    return d.strftime("%d-%m-%y")


def slight_price_variation(price):
    """Apply a small random variation (±5%) to the base price and round to integer."""
    pct = random.uniform(-0.05, 0.05)
    new_price = int(round(price * (1 + pct)))
    return max(1, new_price)


def generate_row(i, start_date, end_date):
    order_id = f"ORD{i:04d}"
    date = random_date(start_date, end_date)
    product, category, base_price = random.choice(PRODUCTS)
    price = slight_price_variation(base_price)

    # Quantity distribution depends on category
    if category == "Electronics":
        qty = random.choices([1,2,3,4,5], weights=[40,25,15,10,10])[0]
    elif category == "Home Appliances":
        qty = random.choices([1,2,3,4,5], weights=[70,15,7,5,3])[0]
    elif category == "Books":
        qty = random.randint(1,5)
    else:  # Clothing, Footwear
        qty = random.randint(1,5)

    total_sales = price * qty

    customer_name = f"{random.choice(CUSTOMER_FIRST)} {random.choice(CUSTOMER_LAST)}"
    location = random.choice(LOCATIONS)
    payment = random.choice(PAYMENT_METHODS)
    status = random.choices(STATUS, weights=[60,25,15])[0]  # more Completed

    return [order_id, date, product, category, price, qty, total_sales, customer_name, location, payment, status]


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Amazon sales CSV data.")
    parser.add_argument("--rows", type=int, default=5000, help="Number of rows to generate (default 5000)")
    parser.add_argument("--output", default="data/amazon_sales_data_2025_synthetic.csv", help="Output CSV path")
    args = parser.parse_args()

    # Choose a date range similar to the example file (Feb 1 2025 - Apr 30 2025)
    start_date = datetime(2025, 2, 1)
    end_date = datetime(2025, 4, 30)

    header = ["Order ID","Date","Product","Category","Price","Quantity","Total Sales","Customer Name","Customer Location","Payment Method","Status"]

    # Ensure output directory exists
    import os
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    with open(args.output, mode="w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(1, args.rows + 1):
            row = generate_row(i, start_date, end_date)
            writer.writerow(row)

    print(f"Generated {args.rows} rows and saved to {args.output}")


if __name__ == "__main__":
    main()
