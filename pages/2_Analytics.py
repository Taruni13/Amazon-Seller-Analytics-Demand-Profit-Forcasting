# pages/2_Analytics.py (Unified Analytics + Modeling)
import streamlit as st
import pandas as pd
import altair as alt
from src.theme import add_custom_css, add_custom_header, add_custom_footer
from src.ml import prepare_tabular, train_models

st.set_page_config(page_title="Analytics & Modeling – Amazon Seller Dashboard", layout="wide")
add_custom_css(show_navbar=False)
add_custom_header('Analytics & Modeling')

st.markdown('<div class="main-block">', unsafe_allow_html=True)

# ---------- DATA LOADERS ----------
@st.cache_data
def load_global_data():
    # Columns per screenshot: region,country,item_type,sales_channel,order_priority,
    # order_date,order_id,ship_date,units_sold,unit_price,unit_cost,total_revenue,total_cost,total_profit
    df = pd.read_csv("data_process/clean_global_sales.csv")
    # Ensure canonical casing
    df.columns = [c.strip() for c in df.columns]
    # Parse order_date and derive Year/Month (string Month for charts)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["Year"] = df["order_date"].dt.year
    df["Month"] = df["order_date"].dt.to_period("M").astype(str)
    # Create display-friendly columns expected by charts/filters
    df["Region"] = df.get("region")
    df["Item Type"] = df.get("item_type")
    df["Sales Channel"] = df.get("sales_channel")
    df["Total Revenue"] = df.get("total_revenue")
    df["Total Profit"] = df.get("total_profit")
    df["Total Cost"] = df.get("total_cost")
    df["Units Sold"] = df.get("units_sold")
    df["Profit Margin"] = (df["Total Profit"] / df["Total Revenue"]).replace([pd.NA, pd.NaT], 0)
    return df

@st.cache_data
def load_retail_data():
    # Columns per screenshot: order_id,date,product,category,price,quantity,total_sales,
    # customer_name,customer_location,payment_method,status
    df = pd.read_csv("data_process/clean_e-commerce_orders.csv")
    df.columns = [c.strip() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["Month"] = df["date"].dt.to_period("M").astype(str)
    # Create display-friendly columns expected by charts/filters
    df["Category"] = df.get("category")
    df["Product"] = df.get("product")
    df["Payment Method"] = df.get("payment_method")
    df["Status"] = df.get("status")
    if "total_sales" in df.columns:
        df["Total Sales"] = df["total_sales"].astype(float)
    else:
        df["Total Sales"] = pd.Series([0.0] * len(df), index=df.index)
    df["Date"] = df["date"]
    return df

global_df = load_global_data()
retail_df = load_retail_data()

# ---------- SIDEBAR ----------
st.sidebar.header("Analytics Filters")
dataset_choice = st.sidebar.radio(
    "Select dataset",
    ["Global Sales (Corporate)", "E-commerce Orders 2025"],
)

# ---------- MAIN ----------
st.title("Analytics & Modeling Overview")

if dataset_choice == "Global Sales (Corporate)":
    st.subheader("Global Sales – Descriptive Analytics")

    # Filters
    regions = st.sidebar.multiselect(
        "Region",
        sorted(global_df["Region"].unique()) if "Region" in global_df.columns else []
    )
    item_types = st.sidebar.multiselect(
        "Item Type",
        sorted(global_df["Item Type"].unique()) if "Item Type" in global_df.columns else []
    )
    channels = st.sidebar.multiselect(
        "Sales Channel",
        sorted(global_df["Sales Channel"].unique()) if "Sales Channel" in global_df.columns else []
    )
    years = st.sidebar.multiselect(
        "Year",
        sorted(global_df["Year"].unique()) if "Year" in global_df.columns else []
    )

    df = global_df.copy()
    if regions:
        df = df[df["Region"].isin(regions)]
    if item_types:
        df = df[df["Item Type"].isin(item_types)]
    if channels:
        df = df[df["Sales Channel"].isin(channels)]
    if years:
        df = df[df["Year"].isin(years)]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Revenue", f"${df.get('Total Revenue', pd.Series(dtype=float)).sum():,.0f}")
    with c2:
        st.metric("Total Profit", f"${df.get('Total Profit', pd.Series(dtype=float)).sum():,.0f}")
    with c3:
        pm = (df.get('Total Profit', pd.Series(dtype=float)) / df.get('Total Revenue', pd.Series(dtype=float)))
        st.metric("Avg Profit Margin", f"{pm.mean() if len(pm)>0 else 0:.2%}")
    with c4:
        st.metric("Total Units Sold", f"{df.get('Units Sold', pd.Series(dtype=float)).sum():,.0f}")

    st.markdown("---")

    # Revenue by Region
    if "Region" in df.columns and "Total Revenue" in df.columns:
        rev_region = df.groupby("Region", as_index=False)["Total Revenue"].sum()
    else:
        rev_region = pd.DataFrame({"Region": [], "Total Revenue": []})
    chart_region = (
        alt.Chart(rev_region)
        .mark_bar()
        .encode(
            x=alt.X("Region", sort="-y"),
            y="Total Revenue",
            tooltip=["Region", "Total Revenue"],
        )
    )
    st.subheader("Revenue by Region")
    st.altair_chart(chart_region, use_container_width=True)

    # Profit by Item Type
    if "Item Type" in df.columns and "Total Profit" in df.columns:
        profit_item = df.groupby("Item Type", as_index=False)["Total Profit"].sum()
    else:
        profit_item = pd.DataFrame({"Item Type": [], "Total Profit": []})
    chart_item = (
        alt.Chart(profit_item)
        .mark_bar()
        .encode(
            x=alt.X("Item Type", sort="-y"),
            y="Total Profit",
            tooltip=["Item Type", "Total Profit"],
        )
    )
    st.subheader("Profit by Item Type")
    st.altair_chart(chart_item, use_container_width=True)

    # Monthly Revenue vs Cost
    monthly = pd.DataFrame({"Month": [], "Total Revenue": [], "Total Cost": []})
    if "Month" in df.columns:
        cols = [c for c in ["Total Revenue", "Total Cost"] if c in df.columns]
        if cols:
            monthly = df.groupby("Month", as_index=False)[cols].sum()
    melted = monthly.melt("Month", var_name="Metric", value_name="Amount")
    chart_month = (
        alt.Chart(melted)
        .mark_line(point=True)
        .encode(
            x="Month",
            y="Amount",
            color="Metric",
            tooltip=["Month", "Metric", "Amount"],
        )
    )
    st.subheader("Monthly Revenue vs Cost")
    st.altair_chart(chart_month, use_container_width=True)

    # Profit Margin Distribution by Item Type
    if "Item Type" in df.columns and "Profit Margin" in df.columns:
        pm_item = df.groupby("Item Type", as_index=False)["Profit Margin"].mean()
    else:
        pm_item = pd.DataFrame({"Item Type": [], "Profit Margin": []})
    chart_pm = (
        alt.Chart(pm_item)
        .mark_bar()
        .encode(
            x=alt.X("Item Type", sort="-y"),
            y="Profit Margin",
            tooltip=["Item Type", "Profit Margin"],
        )
    )
    st.subheader("Average Profit Margin by Item Type")
    st.altair_chart(chart_pm, use_container_width=True)

else:
    st.subheader("E-commerce Orders 2025 – Descriptive Analytics")

    # Filters
    categories = st.sidebar.multiselect(
        "Category", sorted(retail_df["Category"].unique()) if "Category" in retail_df.columns else []
    )
    payment_methods = st.sidebar.multiselect(
        "Payment Method", sorted(retail_df["Payment Method"].unique()) if "Payment Method" in retail_df.columns else []
    )
    statuses = st.sidebar.multiselect(
        "Status", sorted(retail_df["Status"].unique()) if "Status" in retail_df.columns else []
    )

    df = retail_df.copy()
    if categories:
        df = df[df["Category"].isin(categories)]
    if payment_methods:
        df = df[df["Payment Method"].isin(payment_methods)]
    if statuses:
        df = df[df["Status"].isin(statuses)]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Sales", f"${df.get('Total Sales', pd.Series(dtype=float)).sum():,.0f}")
    with c2:
        st.metric("Orders", f"{df.shape[0]:,}")
    with c3:
        avg_order_val = df["Total Sales"].mean() if not df.empty else 0
        st.metric("Avg Order Value", f"${avg_order_val:,.2f}")
    with c4:
        cancel_rate = ((df["Status"] == "Cancelled").mean() if (not df.empty and "Status" in df.columns) else 0)
        st.metric("Cancellation Rate", f"{cancel_rate:.2%}")

    st.markdown("---")

    # Sales by Category
    if "Category" in df.columns and "Total Sales" in df.columns:
        sales_cat = df.groupby("Category", as_index=False)["Total Sales"].sum()
    else:
        sales_cat = pd.DataFrame({"Category": [], "Total Sales": []})
    chart_cat = (
        alt.Chart(sales_cat)
        .mark_bar()
        .encode(
            x=alt.X("Category", sort="-y"),
            y="Total Sales",
            tooltip=["Category", "Total Sales"],
        )
    )
    st.subheader("Sales by Category")
    st.altair_chart(chart_cat, use_container_width=True)

    # Sales by Product
    if "Product" in df.columns and "Total Sales" in df.columns:
        sales_prod = df.groupby("Product", as_index=False)["Total Sales"].sum()
    else:
        sales_prod = pd.DataFrame({"Product": [], "Total Sales": []})
    chart_prod = (
        alt.Chart(sales_prod)
        .mark_bar()
        .encode(
            x=alt.X("Product", sort="-y"),
            y="Total Sales",
            tooltip=["Product", "Total Sales"],
        )
    )
    st.subheader("Sales by Product")
    st.altair_chart(chart_prod, use_container_width=True)

    # Payment Method Distribution
    if "Payment Method" in df.columns:
        pay_counts = df["Payment Method"].value_counts().reset_index()
        pay_counts.columns = ["Payment Method", "Count"]
    else:
        pay_counts = pd.DataFrame({"Payment Method": [], "Count": []})
    chart_pay = (
        alt.Chart(pay_counts)
        .mark_bar()
        .encode(
            x="Payment Method",
            y="Count",
            tooltip=["Payment Method", "Count"],
        )
    )
    st.subheader("Payment Method Distribution")
    st.altair_chart(chart_pay, use_container_width=True)

    # Order Status Breakdown
    if "Status" in df.columns:
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
    else:
        status_counts = pd.DataFrame({"Status": [], "Count": []})
    chart_status = (
        alt.Chart(status_counts)
        .mark_bar()
        .encode(
            x="Status",
            y="Count",
            tooltip=["Status", "Count"],
        )
    )
    st.subheader("Order Status Breakdown")
    st.altair_chart(chart_status, use_container_width=True)

    # Daily Sales Trend
    if "Date" in df.columns:
        daily = df.groupby("Date", as_index=False)["Total Sales"].sum() if "Total Sales" in df.columns else pd.DataFrame({"Date": [], "Total Sales": []})
    elif "date" in df.columns:
        daily = df.groupby("date", as_index=False)["Total Sales"].sum() if "Total Sales" in df.columns else pd.DataFrame({"date": [], "Total Sales": []})
    else:
        daily = pd.DataFrame({"Date": [], "Total Sales": []})
    chart_daily = (
        alt.Chart(daily)
        .mark_line(point=True)
        .encode(
            x="Date",
            y="Total Sales",
            tooltip=["Date", "Total Sales"],
        )
    )
    st.subheader("Daily Sales Trend")
    st.altair_chart(chart_daily, use_container_width=True)

    st.markdown("---")
    st.subheader("🤖 Quick Modeling (on e-commerce dataset)")
    # Minimal supervised modeling using numeric columns
    df_model = df.copy()
    df_model.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df_model.columns]
    numeric_cols = df_model.select_dtypes(include=['number']).columns.tolist()
    if len(numeric_cols) == 0:
        st.info("No numeric columns available for modeling.")
    else:
        target = st.selectbox('Target column', numeric_cols, key='analytics_target')
        drop_cols = st.multiselect('Columns to drop (non-features)',
                                   [c for c in ['order_id','date','customer_name','customer_location'] if c in df_model.columns],
                                   default=[c for c in ['order_id','date'] if c in df_model.columns],
                                   key='analytics_dropcols')
        if st.button('Train models', key='analytics_train'):
            X, y = prepare_tabular(df_model, target=target, drop_cols=drop_cols)
            st.write('Training on', X.shape[0], 'rows and', X.shape[1], 'features')
            results = train_models(X, y, meta={'target': target, 'dataset': 'e-commerce'}, save_path='data/models/model_results.json')
            st.subheader('Results')
            for name, r in results.items():
                st.write(f"**{name}** — MAE: {r['mae']:.2f} RMSE: {r['rmse']:.2f}")
                if hasattr(r['model'], 'feature_importances_'):
                    importances = r['model'].feature_importances_
                    feat_df = pd.DataFrame({'feature': X.columns, 'importance': importances}).sort_values('importance', ascending=False).head(10)
                    st.write('Top features')
                    st.table(feat_df)

st.markdown('</div>', unsafe_allow_html=True)
add_custom_footer()
