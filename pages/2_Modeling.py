import streamlit as st
import pandas as pd
from src.ml import prepare_tabular, train_models
from src.theme import add_custom_css

st.set_page_config(page_title='Modeling', layout='wide')
add_custom_css()

st.title('Modeling')

dataset = st.selectbox('Choose dataset', ['clean_e-commerce_orders.csv', 'clean_global_sales.csv'])
path = f'data_process/{dataset}'
df = pd.read_csv(path)
df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]

st.subheader('Model settings')
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
target = st.selectbox('Target column', numeric_cols)
drop_cols = st.multiselect('Columns to drop (non-features)', ['order_id','date','customer_name','customer_location'], default=['order_id','date'])
run = st.button('Train models')

if run:
    X,y = prepare_tabular(df, target=target, drop_cols=drop_cols)
    st.write('Training on', X.shape[0], 'rows and', X.shape[1], 'features')
    results = train_models(X,y)
    st.subheader('Results')
    for name, r in results.items():
        st.write(f"**{name}** — MAE: {r['mae']:.2f} RMSE: {r['rmse']:.2f}")
        if hasattr(r['model'], 'feature_importances_'):
            importances = r['model'].feature_importances_
            feat_df = pd.DataFrame({'feature': X.columns, 'importance': importances}).sort_values('importance', ascending=False).head(10)
            st.write('Top features')
            st.table(feat_df)
