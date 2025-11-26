"""Streamlit app entry (landing page). Run with: `streamlit run app.py`"""
import streamlit as st
from PIL import Image
from pathlib import Path

# ---------- GLOBAL PAGE CONFIG ----------
st.set_page_config(
    page_title="Amazon Seller Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",

)

def add_custom_css():
    """Add global CSS theme, floating navbar, and footer styles."""
    st.markdown(
        """
        <style>
        :root {
            --pacific-orange: #E87500;
            --pacific-dark: #111111;
            --pacific-light-bg: #faf6f0;
        }

        /* App background */
        .stApp {
            background: var(--pacific-light-bg);
        }

        /* General headings */
        h1, h2, h3, h4 {
            color: var(--pacific-dark);
            font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* --- FLOATING TOP NAVBAR --- */
        .top-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 56px;
            background-color: var(--pacific-dark);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            z-index: 9999;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
        }

        .top-nav-title {
            color: var(--pacific-orange);
            font-weight: 600;
            letter-spacing: 0.04em;
        }

        .top-nav-links a {
            color: #ffffff;
            margin-left: 18px;
            text-decoration: none;
            font-size: 15px;
        }

        .top-nav-links a:hover {
            color: var(--pacific-orange);
            text-decoration: underline;
        }

        /* Push content down so it doesn't hide under navbar.
           Reduced padding to remove excessive whitespace; hide Streamlit's
           default header and menu to avoid double spacing. */
        .top-nav {
            height: 48px;
        }

        .main-block {
            padding-top: 12px !important;
            padding-bottom: 60px; /* space for footer */
            margin-top: 0 !important;
        }

        /* Force-hide various Streamlit header/menu selectors (different versions use different classes) */
        header, header[role="banner"], #MainMenu, .css-18e3th9, .css-1lsmgbg, .reportview-container .main header {display: none !important;}

        /* Zero out Streamlit container padding that can create extra space */
        .reportview-container .main .block-container, .block-container, main > div.reportview-container > section.main {padding-top: 0px !important; margin-top: 0px !important}

        /* Card-style sections */
        .info-card {
            background-color: #f7f7f7;
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid var(--pacific-orange);
            box-shadow: 0 0 8px rgba(0,0,0,0.1);
        }

        /* --- CUSTOM FOOTER --- */
        .custom-footer {
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: var(--pacific-dark);
            color: #ffffff;
            padding: 6px 18px;
            font-size: 13px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 9999;
        }

        .custom-footer a {
            color: var(--pacific-orange);
            text-decoration: none;
        }

        .custom-footer a:hover {
            text-decoration: underline;
        }

        /* Hide default Streamlit footer */
        footer {visibility: hidden;}
        footer:after {content: ""; visibility: hidden;}

        /* --- ENSURE READABLE TEXT IN SYSTEM DARK (NIGHT) MODE --- */
        @media (prefers-color-scheme: dark) {
            :root {
                --pacific-orange: #E87500;
                --pacific-dark: #111111;
                --pacific-light-bg: #faf6f0;
            }

            /* keep your light background, but force dark text for readability */
            .stApp,
            .main-block,
            .info-card,
            .element-container,
            .stMarkdown,
            .stText,
            .stMetric,
            .stTable,
            .stDataFrame,
            .css-1v3fvcr { /* generic Streamlit container selectors */
                background-color: var(--pacific-light-bg) !important;
                color: var(--pacific-dark) !important;
            }

            /* headings, paragraphs, list items, links */
            h1, h2, h3, h4, p, li, span, a, div {
                color: var(--pacific-dark) !important;
            }

            /* override table cells and other common component text */
            th, td, .stDataFrame td, .stDataFrame th {
                color: var(--pacific-dark) !important;
            }

            /* keep navbar/footer contrast */
            .top-nav { background-color: var(--pacific-dark) !important; }
            .top-nav-title { color: var(--pacific-orange) !important; }
            .top-nav-links a { color: #ffffff !important; }
            .custom-footer { background-color: var(--pacific-dark) !important; color: #ffffff !important; }
        }
        """,
        unsafe_allow_html=True,
    )


def home_page():
    add_custom_css()

    # ---------- FLOATING NAVBAR ----------
    st.markdown(
        """
        """,
        unsafe_allow_html=True,
    )

    # ---------- MAIN CONTENT BLOCK ----------
    st.markdown('<div class="main-block">', unsafe_allow_html=True)

    # University logo and title in one horizontal row
    logo_path = Path("assets/pacific_logo.png")
    alt_logo = Path("assets/uop_seal.png")

    # University seal to the left of the title (single logo)
    col_logo, col_title = st.columns([1, 9])
    with col_logo:
        try:
            if logo_path.exists():
                logo = Image.open(logo_path)
                st.image(logo, width=110)
            elif alt_logo.exists():
                logo = Image.open(alt_logo)
                st.image(logo, width=110)
            else:
                st.write("")
        except Exception:
            st.write("")

    with col_title:
        st.markdown(
            """
            <div style="display:flex; flex-direction:column; justify-content:center; height:120px;">
                <h1 style="margin:0; color:#E87500; font-size:36px;" id="overview">Amazon Seller Analytics Dashboard</h1>
                <h3 style="margin:0; color:#444; font-weight:500;">Capstone Project — Demand and Profit Forecasting</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "Welcome! This dashboard lets you explore **Global Amazon sales data** "
        "and **2025 e-commerce amazon order dataset** using interactive filters, KPIs, and charts."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Course + team cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="info-card" id="course-details">
            <h3>Course Details</h3>
            <p><strong>Program:</strong> MSBA – Master of Science in Business Analytics</p>
            <p><strong>Course:</strong> MSBA 286 — Capstone Project II</p>
            <p><strong>Professor:</strong> Prof. Xun Xu</p>
            <p><strong>University:</strong> University of the Pacific</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="info-card" id="team-details">
            <h3>Team Details</h3>
            <p><strong>Group Number:</strong> Group 7</p>
            <p><strong>Team Members:</strong></p>
            <ul>
                <li>Taruniben Atodariya</li>
                <li>Arpitkumar Gohel</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # What you can explore
    st.markdown(
        """
        <h3 style="color:#E87500;">What You Can Explore</h3>
        <ul style="font-size:17px;">
            <li><strong>Global Sales Overview</strong> – Region-wise revenue, profit, and shipping trends</li>
            <li><strong>E-commerce Orders 2025</strong> – Product performance, customer locations, payment behavior</li>
            <li><strong>Comparison & Insights</strong> – Side-by-side KPIs from both datasets</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    # Project Overview
    with st.expander("**Project Overview**", expanded=False):
        st.markdown(
            """
            **Objective**
            
            This capstone project aims to develop a comprehensive analytics dashboard for Amazon sellers, focusing on demand forecasting and profit optimization. By leveraging two distinct datasets—global corporate sales and customer-level e-commerce transactions—the project provides actionable insights into sales trends, product performance, and profitability drivers.
            
            **Key Features**
            
            - **Exploratory Data Analysis (EDA)** – Interactive visualizations and statistical summaries to understand data distributions, patterns, and anomalies
            - **Analytics & Modeling** – Descriptive analytics with KPIs, filters, and charts; supervised machine learning models for predictive insights
            - **Demand & Profit Forecasting** – Time series forecasting using ARIMA and Random Forest models to predict future revenue, profit, and units sold
            - **Insights Dashboard** – Comparative analysis and key takeaways from both datasets to support strategic decision-making
            - **Suggestion System** – User feedback collection to continuously improve the dashboard
            
            **Technologies Used**
            
            - **Python** – pandas, numpy, scikit-learn, statsmodels for data processing and modeling
            - **Streamlit** – interactive web framework for building the dashboard
            - **Altair & Plotly** – data visualization libraries for charts and graphs
            - **Machine Learning** – regression models, time series forecasting, feature importance analysis
            """,
            unsafe_allow_html=True,
        )

    # Dataset details
    with st.expander("**About the Datasets**", expanded=False):
        st.markdown(
            """
            <div id="datasets"></div>

            **Dataset 1** — Amazon Global Sales Dataset (Corporate Sales Analytics)
            A global corporate-style dataset containing region, country, item type, units sold, unit price/cost, revenue, profit, and shipping details.
            It represents high-level operational performance across continents and sales channels, useful for analyzing profitability, geographic trends, and supply-chain efficiency.
            
            **Source:** Kaggle - Amazon Global dataset

            **Dataset 2** — Amazon E-commerce Orders Dataset 2025 (Customer-Level Analytics)
            A retail-level 2025 e-commerce transactions dataset with order ID, product, category, customer name, customer location, payment method, price, quantity, and order status.
            It reflects real-world online shopping behavior, supporting insights into customer preferences, product performance, and cancellation patterns.
            
            **Source:** Kaggle - Amazon / E-commerce Orders 2025
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<br>", unsafe_allow_html=True) 

    # Contact anchor
    st.markdown('<div id="contact"></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close main-block

    # ---------- CUSTOM FOOTER ----------
    st.markdown(
        """
        <div class="custom-footer">
            <span>© 2025 University of the Pacific – MSBA Program</span>
            <span>
                Contact: 
                <a href="mailto:t_atodariya@u.pacific.edu">t_atodariya@u.pacific.edu</a> |
                <a href="mailto:a_gohel@u.pacific.edu">a_gohel@u.pacific.edu</a>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    # Allow running the app both with `streamlit run app.py` and `python app.py`.
    # If executed with plain python, forward to Streamlit's CLI entrypoint.
    # When running under `streamlit run app.py`, Streamlit manages the runtime
    # and will execute this module. To avoid attempting to re-start a nested
    # Streamlit process (which raises "Runtime instance already exists!"), we
    # keep the simple behavior here and render the page directly.
    home_page()

