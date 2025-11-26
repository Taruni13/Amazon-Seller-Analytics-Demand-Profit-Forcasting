import streamlit as st
import pandas as pd
from src.eda import load_csv, normalize_columns, summarize_df, timeseries_aggregate, plot_timeseries, top_n_products
from src.theme import add_custom_css

st.set_page_config(page_title='EDA', layout='wide')
add_custom_css()

st.title('Exploratory Data Analysis')

dataset = st.selectbox('Choose dataset', ['clean_e-commerce_orders.csv', 'clean_global_sales.csv'])
path = f'data_process/{dataset}'

df = load_csv(path)
df = normalize_columns(df)

st.subheader('Sample')
st.dataframe(df.head(100))

st.subheader('Summary Statistics')
head, desc = summarize_df(df)
st.write(desc)

if 'date' in df.columns:
    st.subheader('Time Series')
    # pick numeric column
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if len(numeric_cols) > 0:
        value_col = st.selectbox('Choose value to aggregate', numeric_cols, index=0)
        freq = st.selectbox('Frequency', ['D','W','M'], index=2)
        agg = timeseries_aggregate(df, 'date', value_col, freq=freq)
        st.plotly_chart(plot_timeseries(agg, 'date', value_col))

st.subheader('Top products by sales (if present)')
prod_col = 'product' if 'product' in df.columns else None
if prod_col:
    top = top_n_products(df, product_col=prod_col, value_col='total_sales', n=10)
    st.bar_chart(top.set_index(prod_col))
