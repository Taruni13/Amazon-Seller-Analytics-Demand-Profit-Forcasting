import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

from src.theme import add_custom_css, add_custom_header, add_custom_footer

st.set_page_config(page_title="Forecasting – Amazon Seller Dashboard", layout="wide")
add_custom_css(show_navbar=False)
add_custom_header('Demand & Profit Forecasting')

st.markdown('<div class="main-block">', unsafe_allow_html=True)

# ---------- DATA LOADERS ----------
@st.cache_data
def load_global_data():
    # Schema per screenshot (lowercase with underscores)
    df = pd.read_csv("data_process/clean_global_sales.csv")
    df.columns = [c.strip() for c in df.columns]
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["Month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    # For convenience in metric selection
    df["Total Revenue"] = df.get("total_revenue")
    df["Total Profit"] = df.get("total_profit")
    df["Units Sold"] = df.get("units_sold")
    return df
    df["Month"] = df[date_col].dt.to_period("M").dt.to_timestamp()
    # Harmonize metric column names to expected ones
    if "Total Sales" not in df.columns and "Total Revenue" in df.columns:
        df["Total Sales"] = df["Total Revenue"]
    return df

@st.cache_data
def load_retail_data():
    # Schema per screenshot
    df = pd.read_csv("data_process/clean_e-commerce_orders.csv")
    df.columns = [c.strip() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["Month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    # Convenience metric
    df["Total Sales"] = df.get("total_sales")
    return df
    df["Month"] = df[date_col].dt.to_period("M").dt.to_timestamp()
    # If sales columns differ, map to common name
    if "Total Sales" not in df.columns:
        # Try common alternatives
        for alt in ["sales", "revenue", "Total Revenue"]:
            if alt in df.columns:
                df["Total Sales"] = df[alt]
                break
    return df

global_df = load_global_data()
retail_df = load_retail_data()

# ---------- SIDEBAR ----------
st.sidebar.header("Forecast Settings")

dataset_choice = st.sidebar.radio(
    "Dataset",
    ["Global Sales (Corporate)", "E-commerce Orders 2025"],
)

metric_choice = st.sidebar.selectbox(
    "Metric to forecast",
    ["Total Revenue", "Total Profit", "Units Sold", "Total Sales"],
)

forecast_horizon = st.sidebar.slider(
    "Forecast horizon (months ahead)",
    min_value=3,
    max_value=24,
    value=6,
)

st.title("Demand & Profit Forecasting")

# ---------- BUILD TIME SERIES ----------
if dataset_choice == "Global Sales (Corporate)":
    df = global_df.copy()
    # Exact metric names per global schema
    if metric_choice == "Total Revenue":
        metric = "Total Revenue"
    elif metric_choice == "Total Profit":
        metric = "Total Profit"
    elif metric_choice == "Units Sold":
        metric = "Units Sold"
    else:
        metric = "Total Revenue"
else:
    df = retail_df.copy()
    # Retail schema exposes total_sales only
    metric = "Total Sales"

if metric is None:
    st.error("Selected metric not available in this dataset.")
    st.stop()

if "Month" not in df.columns:
    st.error("No monthly date column available to aggregate.")
    st.stop()

ts = (
    df.groupby("Month", as_index=False)[metric].sum()
    .sort_values("Month")
    .reset_index(drop=True)
)
ts = ts.dropna()

st.subheader(f"Time Series – {metric} (aggregated monthly)")
st.write(ts.tail())

base_chart = (
    alt.Chart(ts)
    .mark_line(point=True)
    .encode(
        x="Month",
        y=metric,
        tooltip=["Month", metric],
    )
)
st.altair_chart(base_chart, use_container_width=True)

# ---------- TRAIN/TEST SPLIT ----------
if len(ts) < 12:
    st.warning("Not enough time points to build a robust forecast. Add more data if possible.")
else:
    train_size = int(len(ts) * 0.8)
    train, test = ts.iloc[:train_size], ts.iloc[train_size:]

    # ---------- ARIMA MODEL ----------
    st.markdown("### ARIMA Forecast")

    # Simple (p,d,q) configuration; you can tune these
    model = ARIMA(train[metric], order=(1, 1, 1))
    arima_res = model.fit()

    arima_pred = arima_res.forecast(steps=len(test))
    arima_rmse = mean_squared_error(test[metric], arima_pred) ** 0.5
    arima_mae = mean_absolute_error(test[metric], arima_pred)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("ARIMA RMSE", f"{arima_rmse:,.2f}")
    with c2:
        st.metric("ARIMA MAE", f"{arima_mae:,.2f}")

    test_arima = test.copy()
    test_arima["ARIMA_Pred"] = arima_pred.values

    chart_arima = (
        alt.Chart(
            pd.concat(
                [
                    train.assign(Type="Train", Pred=train[metric]),
                    test_arima.assign(Type="Test", Pred=test_arima["ARIMA_Pred"]),
                ]
            )
        )
        .mark_line(point=True)
        .encode(
            x="Month",
            y="Pred",
            color="Type",
            tooltip=["Month", "Pred", "Type"],
        )
    )
    st.altair_chart(chart_arima, use_container_width=True)

    # ---------- RANDOM FOREST LAG MODEL ----------
    st.markdown("### Random Forest (Lag-Based) Forecast")

    def make_lag_features(series, n_lags=6):
        df_lag = pd.DataFrame({"y": series})
        for lag in range(1, n_lags + 1):
            df_lag[f"lag_{lag}"] = df_lag["y"].shift(lag)
        return df_lag.dropna()

    lagged = make_lag_features(ts[metric], n_lags=6)
    # Align with original timeline
    lagged["Month"] = ts["Month"].iloc[len(ts) - len(lagged):].values

    train_lag = lagged.iloc[: train_size - 6]
    test_lag = lagged.iloc[train_size - 6 :]

    X_train = train_lag.drop(columns=["y", "Month"])
    y_train = train_lag["y"]
    X_test = test_lag.drop(columns=["y", "Month"])
    y_test = test_lag["y"]

    rf = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
    )
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    rf_rmse = mean_squared_error(y_test, rf_pred) ** 0.5
    rf_mae = mean_absolute_error(y_test, rf_pred)

    c3, c4 = st.columns(2)
    with c3:
        st.metric("Random Forest RMSE", f"{rf_rmse:,.2f}")
    with c4:
        st.metric("Random Forest MAE", f"{rf_mae:,.2f}")

    # Feature importance
    feat_imp = (
        pd.DataFrame(
            {"Feature": X_train.columns, "Importance": rf.feature_importances_}
        )
        .sort_values("Importance", ascending=False)
        .reset_index(drop=True)
    )
    chart_imp = (
        alt.Chart(feat_imp)
        .mark_bar()
        .encode(
            x="Feature",
            y="Importance",
            tooltip=["Feature", "Importance"],
        )
    )
    st.subheader("Random Forest – Lag Feature Importance")
    st.altair_chart(chart_imp, use_container_width=True)

    # Visualize RF predictions vs actual
    rf_df = test_lag[["Month"]].copy()
    rf_df["Actual"] = y_test.values
    rf_df["RF_Pred"] = rf_pred

    chart_rf = (
        alt.Chart(
            rf_df.melt("Month", var_name="Series", value_name="Value")
        )
        .mark_line(point=True)
        .encode(
            x="Month",
            y="Value",
            color="Series",
            tooltip=["Month", "Series", "Value"],
        )
    )
    st.subheader("Random Forest – Actual vs Predicted")
    st.altair_chart(chart_rf, use_container_width=True)

    # ---------- FUTURE FORECAST ----------
    st.markdown("### Future Forecast (Next Months)")

    # Start from last observed value
    last_series = ts[metric].copy()

    # ARIMA future
    arima_future = arima_res.forecast(steps=forecast_horizon)

    # RF future (recursive)
    history = list(last_series.values)
    rf_future = []
    for _ in range(forecast_horizon):
        if len(history) < 6:
            # pad with last value if needed
            history_extended = [history[-1]] * (6 - len(history)) + history
        else:
            history_extended = history
        last_vals = history_extended[-6:]
        X_new = np.array(last_vals).reshape(1, -1)
        y_hat = rf.predict(X_new)[0]
        rf_future.append(y_hat)
        history.append(y_hat)

    last_month = ts["Month"].max()
    future_months = pd.date_range(
        last_month + pd.offsets.MonthBegin(1), periods=forecast_horizon, freq="MS"
    )

    future_df = pd.DataFrame(
        {
            "Month": future_months,
            "ARIMA_Forecast": arima_future.values,
            "RF_Forecast": rf_future,
        }
    )

    chart_future = (
        alt.Chart(
            pd.concat(
                [
                    ts.tail(6).assign(Type="History", Value=ts[metric].tail(6).values),
                    future_df.melt("Month", var_name="Type", value_name="Value"),
                ]
            )
        )
        .mark_line(point=True)
        .encode(
            x="Month",
            y="Value",
            color="Type",
            tooltip=["Month", "Type", "Value"],
        )
    )
    st.subheader(f"Future {forecast_horizon}-Month Forecast")
    st.altair_chart(chart_future, use_container_width=True)

    st.info(
        "Tip: you can export these forecast tables and charts into your report "
        "and compare which model works best for each product group or metric."
    )

st.markdown('</div>', unsafe_allow_html=True)
add_custom_footer()
