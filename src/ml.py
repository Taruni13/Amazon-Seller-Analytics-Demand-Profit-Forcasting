"""Lightweight ML helpers for simple modeling and forecasting used in Streamlit app."""
from typing import Dict, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


def prepare_tabular(df: pd.DataFrame, target: str, drop_cols: list = None) -> Tuple[pd.DataFrame, pd.Series]:
    df = df.copy()
    if drop_cols is None:
        drop_cols = []
    X = df.drop(columns=[c for c in [target] + drop_cols if c in df.columns], errors='ignore')
    # select numeric columns
    X = X.select_dtypes(include=[np.number]).fillna(0)
    y = pd.to_numeric(df[target], errors='coerce').fillna(0)
    return X, y


def train_models(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42) -> Dict[str, dict]:
    results = {}
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    models = {
        'LinearRegression': LinearRegression(),
        'RandomForest': RandomForestRegressor(n_estimators=50, random_state=random_state),
        'GradientBoosting': GradientBoostingRegressor(n_estimators=50, random_state=random_state),
    }

    for name, m in models.items():
        m.fit(X_train, y_train)
        y_pred = m.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        # some sklearn versions don't accept the `squared` kwarg — compute RMSE manually
        mse = mean_squared_error(y_test, y_pred)
        rmse = float(np.sqrt(mse))
        results[name] = {'model': m, 'mae': mae, 'rmse': rmse}

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
