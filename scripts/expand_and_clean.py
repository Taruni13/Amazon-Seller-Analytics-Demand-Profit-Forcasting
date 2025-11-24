#!/usr/bin/env python3
"""
Expand (to 5000 rows) and clean multiple CSV files of differing schemas.

Usage:
    python scripts/expand_and_clean.py --inputs raw_data/e-commerce_orders.csv raw_data/global_sales.csv --rows 5000 --output_dir data_process

This will create cleaned files named `clean_<original_filename>` in `data_process/`.

The script:
- Loads each input CSV
- If rows < target, augments by sampling+perturbation until target rows
- If rows >= target, samples down to target (random sample)
- Applies cleaning: normalize column names, parse dates, ensure numeric types, recompute totals where possible, strip whitespace, standardize a few common fields
- Writes `data_process/clean_<original_filename>`
"""

import os
import argparse
import random
from datetime import timedelta
import pandas as pd
import numpy as np


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    return df


def detect_date_columns(df: pd.DataFrame):
    return [c for c in df.columns if 'date' in c]


def parse_dates(df: pd.DataFrame):
    df = df.copy()
    date_cols = detect_date_columns(df)
    for c in date_cols:
        # try multiple common formats
        df[c] = pd.to_datetime(df[c], dayfirst=False, errors='coerce')
        # if many NaT, try dayfirst=True
        if df[c].isna().mean() > 0.5:
            df[c] = pd.to_datetime(df[c], dayfirst=True, errors='coerce')
    return df


def ensure_numeric(df: pd.DataFrame):
    df = df.copy()
    for c in df.columns:
        if c in ['price','unit_price','unit_cost','quantity','units_sold','total_sales','total_revenue','total_cost','total_profit']:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    return df


def recompute_totals(df: pd.DataFrame):
    df = df.copy()
    # Handle common patterns: price * quantity -> total_sales/total_revenue
    if 'price' in df.columns and 'quantity' in df.columns:
        recomputed = df['price'] * df['quantity']
        if 'total_sales' in df.columns:
            mask = df['total_sales'].isna() | ( (df['total_sales'] - recomputed).abs() > 0.01 )
            df.loc[mask, 'total_sales'] = recomputed[mask]
        elif 'total_revenue' in df.columns:
            mask = df['total_revenue'].isna() | ( (df['total_revenue'] - recomputed).abs() > 0.01 )
            df.loc[mask, 'total_revenue'] = recomputed[mask]
    # If unit_price and units_sold exist, fill total_revenue
    if 'unit_price' in df.columns and 'units_sold' in df.columns and 'total_revenue' in df.columns:
        recomputed = df['unit_price'] * df['units_sold']
        mask = df['total_revenue'].isna() | ( (df['total_revenue'] - recomputed).abs() > 0.01 )
        df.loc[mask, 'total_revenue'] = recomputed[mask]
    return df


def clean_text_fields(df: pd.DataFrame):
    df = df.copy()
    for c in df.select_dtypes(include=['object']).columns:
        df[c] = df[c].astype(str).str.strip()
    return df


def standardize_values(df: pd.DataFrame):
    df = df.copy()
    # standardize status/payment/order_priority if present
    if 'order_priority' in df.columns:
        df['order_priority'] = df['order_priority'].astype(str).str.upper().str.strip()
    if 'payment_method' in df.columns:
        df['payment_method'] = df['payment_method'].astype(str).str.title().str.strip()
    if 'status' in df.columns:
        df['status'] = df['status'].astype(str).str.title().str.strip()
    return df


def perturb_row(row: pd.Series, numeric_cols, date_cols):
    r = row.copy()
    # numeric perturbation: small gaussian noise (5%)
    for c in numeric_cols:
        if pd.notna(r.get(c, None)):
            try:
                val = float(r[c])
                noise = np.random.normal(loc=1.0, scale=0.05)
                new = val * noise
                # preserve integer nature for counts
                if float(val).is_integer():
                    r[c] = int(max(0, round(new)))
                else:
                    r[c] = round(max(0, new), 2)
            except Exception:
                pass
    # date perturbation: shift by -7..7 days
    for c in date_cols:
        try:
            if pd.notna(r.get(c, None)):
                d = pd.to_datetime(r[c], errors='coerce')
                if not pd.isna(d):
                    shift = random.randint(-7, 7)
                    r[c] = (d + timedelta(days=shift))
        except Exception:
            pass
    # small changes to categorical fields: sometimes swap to another existing value (handled at caller)
    return r


def expand_to_n(df: pd.DataFrame, n: int, seed=0) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)
    if len(df) >= n:
        return df.sample(n=n, random_state=seed).reset_index(drop=True)

    rows = df.copy().reset_index(drop=True)
    numeric_cols = [c for c in rows.columns if rows[c].dtype.kind in 'biufc' or c in ['price','quantity','total_sales','unit_price','units_sold','unit_cost','total_revenue']]
    date_cols = detect_date_columns(rows)

    i = 0
    while len(rows) < n:
        src_idx = random.randint(0, len(df)-1)
        row = df.iloc[src_idx]
        new_row = perturb_row(row, numeric_cols, date_cols)
        # make a new order id if column present
        if 'order_id' in rows.columns:
            new_row['order_id'] = f"SYN{len(rows)+1:06d}"
        # append new_row as a single-row DataFrame (DataFrame.append is deprecated)
        rows = pd.concat([rows, pd.DataFrame([new_row])], ignore_index=True)
        i += 1
        if i > n*10:
            break
    # final cleanup: ensure length n
    return rows.head(n).reset_index(drop=True)


def process_file(path: str, target_rows: int, output_dir: str):
    name = os.path.basename(path)
    print(f"Processing {name}")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"  Failed to read {path}: {e}")
        return

    df = normalize_columns(df)

    # Expand or sample
    df_expanded = expand_to_n(df, target_rows)

    # Clean pipeline
    df_expanded = parse_dates(df_expanded)
    df_expanded = clean_text_fields(df_expanded)
    df_expanded = ensure_numeric(df_expanded)
    df_expanded = recompute_totals(df_expanded)
    df_expanded = standardize_values(df_expanded)

    # prepare output path
    os.makedirs(output_dir, exist_ok=True)
    out_name = f"clean_{name}"
    out_path = os.path.join(output_dir, out_name)
    df_expanded.to_csv(out_path, index=False)
    print(f"  Saved cleaned file to {out_path}")


def main():
    parser = argparse.ArgumentParser(description='Expand and clean CSV files')
    parser.add_argument('--inputs', nargs='+', required=True, help='Input CSV paths')
    parser.add_argument('--rows', type=int, default=5000, help='Target row count per file')
    parser.add_argument('--output_dir', default='data_process', help='Directory to save cleaned files')
    args = parser.parse_args()

    for p in args.inputs:
        process_file(p, args.rows, args.output_dir)


if __name__ == '__main__':
    main()
