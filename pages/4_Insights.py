import streamlit as st
import pandas as pd
from src.theme import add_custom_css, add_custom_header, add_custom_footer

st.set_page_config(page_title='Insights', layout='wide')
add_custom_css(show_navbar=False)
add_custom_header('Business Insights')

st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.title('Business Insights')

dataset = st.selectbox('Choose dataset', ['clean_e-commerce_orders.csv', 'clean_global_sales.csv'])
path = f'data_process/{dataset}'
df = pd.read_csv(path)
df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]

st.subheader('Top SKUs / Items by revenue')
if 'product' in df.columns and 'total_sales' in df.columns:
    top = df.groupby('product')['total_sales'].sum().sort_values(ascending=False).head(10).reset_index()
    st.table(top)
elif 'item_type' in df.columns and 'total_revenue' in df.columns:
    top = df.groupby('item_type')['total_revenue'].sum().sort_values(ascending=False).head(10).reset_index()
    st.table(top)
else:
    st.write('No product/item revenue columns found')

st.subheader('Profitability by location')
if 'customer_location' in df.columns and 'total_sales' in df.columns:
    loc = df.groupby('customer_location')['total_sales'].sum().sort_values(ascending=False).head(10).reset_index()
    st.table(loc)
elif 'country' in df.columns and 'total_profit' in df.columns:
    loc = df.groupby('country')['total_profit'].sum().sort_values(ascending=False).head(10).reset_index()
    st.table(loc)
else:
    st.write('No location profitability columns found')

st.markdown('</div>', unsafe_allow_html=True)
add_custom_footer()
