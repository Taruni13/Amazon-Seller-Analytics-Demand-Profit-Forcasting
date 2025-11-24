#!/usr/bin/env python3
"""
Simple cleaning pipeline for the synthetic Amazon sales CSV.
Reads:  data/amazon_sales_data_2025_synthetic.csv
Writes: data/processed/amazon_sales_data_2025_cleaned.csv

Cleaning steps:
- Normalize column names
- Parse `Date` to ISO date `YYYY-MM-DD`
- Ensure numeric types for `Price`, `Quantity`, `Total Sales`
- Recompute `Total Sales` if inconsistent
- Strip whitespace from text fields
- Drop duplicates and rows with missing critical fields
- Standardize `Payment Method` and `Status` values
"""

import os
import pandas as pd

INPUT_PATH = "data/amazon_sales_data_2025_synthetic.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "amazon_sales_data_2025_cleaned.csv")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Original format is dd-mm-yy (e.g., 14-03-25). We'll parse accordingly.
    def to_iso(x):
        try:
            return pd.to_datetime(x, format="%d-%m-%y", errors="coerce").date().isoformat()
        except Exception:
            return pd.NaT

    if "date" in df.columns:
        df["date"] = df["date"].apply(lambda x: to_iso(x) if pd.notna(x) else pd.NaT)
    return df


def ensure_numeric(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["price", "quantity", "total_sales"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def recompute_total_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if all(c in df.columns for c in ["price", "quantity"]):
        recomputed = df["price"] * df["quantity"]
        # If total_sales is NaN or differs significantly, replace it
        if "total_sales" not in df.columns:
            df["total_sales"] = recomputed
        else:
            diff = (df["total_sales"] - recomputed).abs()
            mask = df["total_sales"].isna() | (diff > 0.01)
            df.loc[mask, "total_sales"] = recomputed[mask]
    return df


def clean_text_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    text_cols = [c for c in df.columns if df[c].dtype == object]
    for c in text_cols:
        df[c] = df[c].astype(str).str.strip()
    return df


def standardize_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "payment_method" in df.columns:
        # Map common variants to canonical forms
        mapping = {
            "debit card": "Debit Card",
            "credit card": "Credit Card",
            "paypal": "PayPal",
            "amazon pay": "Amazon Pay",
            "gift card": "Gift Card",
        }
        df["payment_method"] = df["payment_method"].str.lower().map(mapping).fillna(df["payment_method"])

    if "status" in df.columns:
        mapping = {"completed": "Completed", "pending": "Pending", "cancelled": "Cancelled"}
        df["status"] = df["status"].str.lower().map(mapping).fillna(df["status"])

    return df


def drop_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Drop rows missing critical fields: order_id, date, product, price, quantity
    critical = ["order_id", "date", "product", "price", "quantity"]
    missing_critical = df[critical].isna().any(axis=1)
    df = df.loc[~missing_critical].reset_index(drop=True)
    # Drop duplicates based on order_id
    if "order_id" in df.columns:
        df = df.drop_duplicates(subset=["order_id"])
    return df


def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Input file not found: {INPUT_PATH}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(INPUT_PATH, dtype=str)

    df = normalize_columns(df)
    df = parse_dates(df)
    df = ensure_numeric(df)
    df = recompute_total_sales(df)
    df = clean_text_fields(df)
    df = standardize_values(df)
    df = drop_invalid_rows(df)

    # Reorder columns to a sensible order
    cols = [c for c in ["order_id", "date", "product", "category", "price", "quantity", "total_sales", "customer_name", "customer_location", "payment_method", "status"] if c in df.columns]
    df = df[cols]

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned data saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
