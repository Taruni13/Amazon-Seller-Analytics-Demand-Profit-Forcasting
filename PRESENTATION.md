---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  h1 {
    color: #E87500;
  }
  h2 {
    color: #111111;
  }
---

# Amazon Seller Analytics
## Demand and Profit Forecasting Dashboard

**MSBA 286 — Capstone Project II**  
University of the Pacific — Fall 2025

**Group 7**
- Taruniben Atodariya (Group Leader)
- Arpitkumar Gohel (Team Member)

---

# Project Overview

## What We Built
**End-to-end interactive analytics dashboard** for Amazon sellers

### Key Features
- ✅ Exploratory Data Analysis (EDA)
- ✅ Machine Learning Predictive Modeling
- ✅ Time-Series Forecasting
- ✅ Actionable Business Recommendations

### Data Scale
- **45,000+** transactional records
- **2 comprehensive datasets** (Global Sales + E-Commerce Orders)
- **12-month** time period coverage

---

# Problem Statement & Objectives

## Critical Business Questions
1. **Which products and regions** generate the most revenue and profit?
2. **Can we reliably forecast** demand and profit for 3-6 months?
3. **Which features** (price, channel, category) most influence revenue?

## Solution Approach
- Integrate multiple data sources into unified platform
- Apply ML and time-series forecasting
- Deliver interactive dashboard with prescriptive insights

---

# Data Sources & Preparation

## Datasets
**Global Sales** - Corporate-level (45,000+ records)
- Region, Country, Item Type, Sales Channel
- Units Sold, Revenue, Cost, Profit

**E-Commerce Orders** - Retail-level (2025 orders)
- Product, Category, Price, Quantity
- Customer Location, Payment Method

## Feature Engineering
- **Profit Margin** = (Price - Cost) / Price
- **Demand Index** = Sales Volume + Ratings + Reviews
- **Price Elasticity Score** = % Sales Change / % Price Change

---

# Methodology & Models

## Three-Pronged Approach

### 1️⃣ Exploratory Data Analysis
Descriptive statistics, time-series trends, top-N rankings

### 2️⃣ Predictive Modeling (Supervised ML)
- **Random Forest Regressor** - Best overall (R² ≈ 0.85-0.87)
- **Gradient Boosting** - Complex interactions
- **Linear Regression** - Baseline comparison

### 3️⃣ Time-Series Forecasting
- **ARIMA** - Seasonal patterns (R² ≈ 0.78-0.82)
- **Hybrid ARIMA-LSTM** - Highest accuracy (R² ≈ 0.87)

---

# Dashboard Features

## 6 Interactive Pages

| Page | Purpose |
|------|---------|
| **Home** | Overview and navigation |
| **EDA** | Data exploration and visualization |
| **Analytics** | ML model training and comparison |
| **Forecasting** | 3-6 month demand/profit predictions |
| **Insights** | Aggregated KPIs and findings |
| **Suggestions** | User feedback collection |

**Tech Stack:** Streamlit, Python 3.11, Scikit-learn, Statsmodels

---

# Key Findings

## 1. Forecasting Performance
- **LSTM: R² = 0.87** (highest accuracy)
- Reliable 3-6 month forecasts for inventory planning

## 2. Optimal Pricing Strategy
- **10-20% discounts** increase demand while preserving profit
- Deep discounts (>30%) harm long-term margins

## 3. Social Proof Impact
- **r = 0.62 correlation** between ratings and sales
- Review volume drives purchasing decisions

## 4. Category Performance
- **Electronics & Home:** Stable margins, consistent demand
- **Fashion:** Higher volatility, dynamic pricing opportunity

---

# Business Recommendations

## Pricing Strategy
✅ Implement **dynamic pricing** using ML models  
✅ Target **10-20% discount range** for promotions  
✅ Category-specific pricing (Electronics: volume, Fashion: seasonal)

## Inventory Management
✅ Use **3-6 month forecasts** for purchase planning  
✅ Maintain safety stock based on demand volatility  
✅ Prioritize high-margin, high-demand items

## Marketing
✅ Actively solicit **product reviews**  
✅ Highlight top-rated products  
✅ Balance online volume with offline margins

---

# Technical Architecture

```
├── App.py                    # Dashboard entry
├── pages/
│   ├── 1_EDA.py             # Exploratory analysis
│   ├── 2_Analytics.py       # ML modeling
│   ├── 3_Forecasting.py     # Time-series
│   ├── 4_Insights.py        # KPIs
│   └── 5_Suggestion.py      # Feedback
├── src/
│   ├── eda.py, ml.py, theme.py
└── data_process/
    ├── clean_global_sales.csv
    └── clean_e-commerce_orders.csv
```

**Deployment:** Streamlit Community Cloud | **Repo:** github.com/Taruni13

---

# Results & Impact

## Quantitative Outcomes
- **Revenue forecast error:** < 15% MAE
- **Demand prediction:** R² = 0.87
- **Profit margin prediction:** R² = 0.82

## Business Impact
- Identified **20% of products** generating **80% of profit**
- Discovered optimal discount range (**10-20%**)
- Quantified rating impact (**+62% correlation**)

## Academic Rigor
- Literature-backed methodology (7 research papers)
- Validated with cross-validation and robustness checks
- Production-ready analytics platform

---

# Thank You!

## Amazon Seller Analytics Dashboard
**Empowering Data-Driven Decisions for E-Commerce Success**

### Questions?

**Contact:**
- Taruniben Atodariya (Group Leader)
- Arpitkumar Gohel (Team Member)

**Resources:**
- GitHub: Taruni13/Amazon-Seller-Analytics-Demand-Profit-Forcasting
- Dashboard: Streamlit Community Cloud
- Report: REPORT.md

---
