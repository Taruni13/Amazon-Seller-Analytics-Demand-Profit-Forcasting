import streamlit as st
import pandas as pd
import numpy as np
from src.ml import forecast_with_linear_regression
from src.theme import add_custom_css

st.set_page_config(page_title='Forecast', layout='wide')
add_custom_css()

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
        preds = forecast_with_linear_regression(agg, forecast_steps=int(steps), lags=7)
        last_date = agg.index.max()
        # For monthly frequencies use DateOffset because Timedelta('1M') is ambiguous
        if freq == 'D':
            start = last_date + pd.Timedelta(days=1)
        elif freq == 'W':
            start = last_date + pd.Timedelta(weeks=1)
        elif freq == 'M':
            start = last_date + pd.DateOffset(months=1)
        else:
            # Fallback: try one day
            start = last_date + pd.Timedelta(days=1)

        dates = pd.date_range(start=start, periods=len(preds), freq=freq)
        res = pd.Series(preds, index=dates)
        st.line_chart(pd.concat([agg, res]))
