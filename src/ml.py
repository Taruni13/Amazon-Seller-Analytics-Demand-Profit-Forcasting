"""Lightweight ML helpers for simple modeling and forecasting used in Streamlit app."""
from typing import Dict, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json
import os
from datetime import datetime


def prepare_tabular(df: pd.DataFrame, target: str, drop_cols: list = None) -> Tuple[pd.DataFrame, pd.Series]:
    df = df.copy()
    if drop_cols is None:
        drop_cols = []
    X = df.drop(columns=[c for c in [target] + drop_cols if c in df.columns], errors='ignore')
    # select numeric columns
    X = X.select_dtypes(include=[np.number]).fillna(0)
    y = pd.to_numeric(df[target], errors='coerce').fillna(0)
    return X, y


def train_models(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42,
                 meta: dict = None, save_path: str = "data/models/model_results.json") -> Dict[str, dict]:
    """Train baseline models and save serializable metrics to disk.

    Parameters:
    - X, y: training data
    - test_size, random_state: passed to train_test_split
    - meta: optional dict saved alongside the results (e.g., target name, dataset)
    - save_path: JSON file path where results are appended

    Returns dict of trained models and metrics (model objects are returned for immediate UI use).
    """
    results = {}
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    models = {
        'LinearRegression': LinearRegression(),
        'RandomForest': RandomForestRegressor(n_estimators=50, random_state=random_state),
        'GradientBoosting': GradientBoostingRegressor(n_estimators=50, random_state=random_state),
    }

    serializable_results = {}

    for name, m in models.items():
        m.fit(X_train, y_train)
        y_pred = m.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = float(np.sqrt(mse))
        results[name] = {'model': m, 'mae': mae, 'rmse': rmse}

        # Prepare serializable slice for disk (no model objects)
        fi = None
        if hasattr(m, 'feature_importances_'):
            try:
                fi = [float(x) for x in m.feature_importances_.tolist()]
            except Exception:
                fi = None

        serializable_results[name] = {
            'mae': float(mae),
            'rmse': float(rmse),
            'feature_importances': fi,
        }

    # Save results to disk (append entry)
    try:
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'meta': meta or {},
            'n_features': int(X.shape[1]) if hasattr(X, 'shape') else None,
            'n_rows': int(X.shape[0]) if hasattr(X, 'shape') else None,
            'results': serializable_results,
        }

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        if os.path.exists(save_path):
            try:
                with open(save_path, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
            except Exception:
                data = []
        else:
            data = []

        data.append(entry)
        with open(save_path, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, indent=2)
    except Exception:
        # don't break training if saving fails — silently continue
        pass

    return results


def simple_lag_features(series: pd.Series, lags: int = 7) -> pd.DataFrame:
    df = pd.DataFrame({'y': series.values})
    for lag in range(1, lags + 1):
        df[f'lag_{lag}'] = df['y'].shift(lag)
    df = df.dropna().reset_index(drop=True)
    return df


def forecast_with_linear_regression(series: pd.Series, forecast_steps: int = 30, lags: int = 7) -> np.ndarray:
    df = simple_lag_features(series, lags=lags)
    X = df.drop(columns=['y']).values
    y = df['y'].values
    model = LinearRegression()
    model.fit(X, y)
    last_vals = series.values[-lags:]
    preds = []
    current = list(last_vals)
    for _ in range(forecast_steps):
        x = np.array(current[-lags:]).reshape(1, -1)
        p = model.predict(x)[0]
        preds.append(p)
        current.append(p)
    return np.array(preds)
