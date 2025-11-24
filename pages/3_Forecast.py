import streamlit as st
import pandas as pd
import numpy as np
from src.ml import forecast_with_linear_regression

st.title('Forecast')

dataset = st.selectbox('Choose dataset (time series)', ['clean_e-commerce_orders.csv', 'clean_global_sales.csv'])
path = f'data_process/{dataset}'
df = pd.read_csv(path)
df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]

if 'date' not in df.columns:
    st.warning('No `date` column found in this dataset')
else:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    st.subheader('Aggregate time series')
    value_col = st.selectbox('Value to aggregate', df.select_dtypes(include=[np.number]).columns.tolist())
    freq = st.selectbox('Frequency', ['D','W','M'], index=2)
    agg = df.set_index('date').resample(freq)[value_col].sum().dropna()
    st.line_chart(agg)

    steps = st.number_input('Forecast steps', min_value=7, max_value=365, value=30)
    if st.button('Run simple lag-based forecast'):
        preds = forecast_with_linear_regression(agg, forecast_steps=steps, lags=7)
        last_date = agg.index.max()
        dates = pd.date_range(start=last_date + pd.Timedelta(1, unit=freq), periods=len(preds), freq=freq)
        res = pd.Series(preds, index=dates)
        st.line_chart(pd.concat([agg, res]))
