import streamlit as st
import pandas as pd
from src.theme import add_custom_css, add_custom_header, add_custom_footer

st.set_page_config(page_title='Insights', layout='wide')
add_custom_css(show_navbar=False)
add_custom_header('Business Insights')

st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.title('Business Insights')

# Project Summary & Results (aggregated KPIs + methods summary)
with st.expander('Project Summary & Results', expanded=True):
    st.markdown('''
    **What this page shows**

    - Quick, consolidated project summary: datasets, methods used, and overall results.
    - Aggregated KPIs computed from available datasets (global sales and e‑commerce orders).
    - Short, actionable findings and where to find detailed model/forecast outputs.
    ''')

    # Load datasets (best-effort, handle missing columns)
    try:
        gpath = 'data_process/clean_global_sales.csv'
        rpath = 'data_process/clean_e-commerce_orders.csv'
        gdf = pd.read_csv(gpath)
        rdf = pd.read_csv(rpath)
    except Exception:
        gdf = pd.DataFrame()
        rdf = pd.DataFrame()

    # Normalize column names for safe access
    def _norm_cols(df):
        df = df.copy()
        df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]
        return df

    gdf = _norm_cols(gdf) if not gdf.empty else gdf
    rdf = _norm_cols(rdf) if not rdf.empty else rdf

    # Compute aggregated KPIs
    kpis = {}
    if not gdf.empty:
        if 'total_revenue' in gdf.columns:
            kpis['global_total_revenue'] = float(gdf['total_revenue'].dropna().astype(float).sum())
        if 'total_profit' in gdf.columns:
            kpis['global_total_profit'] = float(gdf['total_profit'].dropna().astype(float).sum())
        if 'units_sold' in gdf.columns:
            kpis['global_units_sold'] = int(gdf['units_sold'].dropna().astype(int).sum())

    if not rdf.empty:
        if 'total_sales' in rdf.columns:
            kpis['retail_total_sales'] = float(rdf['total_sales'].dropna().astype(float).sum())
        if 'quantity' in rdf.columns:
            kpis['retail_total_orders'] = int(rdf['quantity'].dropna().astype(int).sum())

    # Display KPIs
    if kpis:
        cols = st.columns(len(kpis))
        for i, (k, v) in enumerate(kpis.items()):
            label = k.replace('_', ' ').title()
            cols[i].metric(label, f"{v:,.0f}")
    else:
        st.info('No data available to compute aggregate KPIs. Ensure CSV files are present in `data_process/`.')

    # Methods and results summary (descriptive)
    st.markdown('''
    **Methods Used**

    - Exploratory Data Analysis (EDA): descriptive statistics, time-series aggregation, top‑N product/location ranking, missing-value checks and distribution plots.
    - Analytics / Modeling: tabular feature engineering and supervised models (Random Forest and other regressors). Use the *Analytics & Modeling* page to run model training and view MAE/RMSE and feature importances.
    - Forecasting: time-series approaches including ARIMA and Random Forest-based forecasting for revenue/profit/units. Use the *Forecasting* page to generate horizon forecasts and compare model errors.

    **How to interpret results**

    - For model performance (MAE/RMSE) and feature importances, open the *Analytics & Modeling* page and run training for the selected target.
    - For per-product or per-region forecasts, open the *Forecasting* page and select the metric and product/group of interest.
    ''', unsafe_allow_html=True)

    st.markdown('---')

    # Quick actionable findings placeholder (users can update after running models)
    st.markdown('''
    **Quick Findings (computed)**

    - The aggregated KPIs above summarize total revenue, profit, and sales across both datasets (if present).
    - Detailed, model-level results are produced interactively when models are trained on the *Analytics & Modeling* and *Forecasting* pages.
    ''', unsafe_allow_html=True)

    # Load and display saved model metrics (if present)
    import json, os
    results_path = 'data/models/model_results.json'
    if os.path.exists(results_path):
        try:
            with open(results_path, 'r', encoding='utf-8') as fh:
                runs = json.load(fh)
        except Exception:
            runs = []

        if runs:
            latest = runs[-1]
            st.markdown('---')
            st.markdown(f"**Latest Model Run** — {latest.get('timestamp', '')}")
            meta = latest.get('meta', {})
            if meta:
                st.write('Run meta:', meta)

            res = latest.get('results', {})
            for model_name, metrics in res.items():
                cols = st.columns([2, 1, 1])
                cols[0].write(f"**{model_name}**")
                cols[1].metric('MAE', f"{metrics.get('mae', 0):.3f}")
                cols[2].metric('RMSE', f"{metrics.get('rmse', 0):.3f}")

                # If feature importances were saved, show top 5 with feature names if available
                fi = metrics.get('feature_importances')
                if fi:
                    # Attempt to show feature names by reading last training metadata (not always available)
                    try:
                        # If feature names were stored in meta, use them; otherwise show index-based ranks
                        feature_names = meta.get('feature_names') if isinstance(meta, dict) else None
                        if feature_names and len(feature_names) == len(fi):
                            feat_df = pd.DataFrame({'feature': feature_names, 'importance': fi}).sort_values('importance', ascending=False).head(10)
                        else:
                            feat_df = pd.DataFrame({'feature': [f'feature_{i}' for i in range(len(fi))], 'importance': fi}).sort_values('importance', ascending=False).head(10)
                        st.table(feat_df)
                    except Exception:
                        pass

            # Show history table (timestamps and a simple metric like best RMSE)
            try:
                history = []
                for r in runs[-10:]:
                    best_rmse = None
                    for m in r.get('results', {}).values():
                        if best_rmse is None or (m.get('rmse') is not None and m.get('rmse') < best_rmse):
                            best_rmse = m.get('rmse')
                    history.append({'timestamp': r.get('timestamp'), 'best_rmse': best_rmse, 'meta': r.get('meta', {})})
                hist_df = pd.DataFrame(history)
                st.subheader('Recent Model Runs')
                st.table(hist_df.sort_values('timestamp', ascending=False))
            except Exception:
                pass


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
