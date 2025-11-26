"""Basic EDA helpers for the project.
"""
from typing import Tuple
import pandas as pd
import plotly.express as px


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    return df


def summarize_df(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return head and descriptive stats (numeric)"""
    return df.head(), df.describe(include='all')


def timeseries_aggregate(df: pd.DataFrame, date_col: str, value_col: str, freq: str = 'D') -> pd.DataFrame:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    # Use 'MS' instead of 'M' to avoid FutureWarning
    resample_freq = 'MS' if freq == 'M' else freq
    agg = df.set_index(date_col).resample(resample_freq)[value_col].sum().reset_index()
    return agg


def plot_timeseries(df: pd.DataFrame, date_col: str, value_col: str, title: str = None):
    fig = px.line(df, x=date_col, y=value_col, title=title or f'{value_col} over time')
    return fig


def top_n_products(df: pd.DataFrame, product_col: str = 'product', value_col: str = 'total_sales', n: int = 10):
    if product_col not in df.columns or value_col not in df.columns:
        return pd.DataFrame()
    s = df.groupby(product_col)[value_col].sum().sort_values(ascending=False).head(n).reset_index()
    return s
