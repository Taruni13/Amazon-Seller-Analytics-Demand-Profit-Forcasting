MSBA 286 — Capstone Final Project Report
Group 7 — Amazon Seller Analytics Dashboard

Title: Amazon Seller Analytics Dashboard — Demand and Profit Forecasting

Group Members:
- Taruniben Atodariya — ID: [ID]
- Arpitkumar Gohel — ID: [ID]

Course: MSBA 286 — Capstone Project II (Section 1)
University of the Pacific — Fall 2025

=================================================================

Abstract

This project develops an end-to-end analytics dashboard for Amazon sellers that combines two datasets — a corporate-style global sales dataset and a 2025 e-commerce orders dataset — to provide descriptive analytics, machine-learning-based modeling, and time-series forecasting for demand and profit optimization. The dashboard integrates exploratory data analysis, supervised learning (Random Forest, Linear Regression, Gradient Boosting), and time-series forecasting (ARIMA and lag-based regression), offering actionable insights and recommendations for merchandizing and pricing.

Keywords

Amazon, demand forecasting, profit optimization, time series, Random Forest, ARIMA, analytics dashboard

=================================================================

1. Introduction / Background

1.1 Objective

The objective of this capstone project is to build an interactive analytics product to help Amazon sellers make decisions about inventory, pricing, and product focus. The dashboard must:
- Provide exploratory visualizations and KPIs that summarize historical performance.
- Train simple supervised models to predict sales-related targets and surface feature importances.
- Produce short-term forecasts for revenue, profit, and units sold to inform ordering and promotions.

1.2 Research questions

- Which products and regions produce the most revenue and profit?
- Can we forecast demand and profit reliably for the next 3-6 months?
- Which features (price, channel, product category) are the most predictive of revenue and profit?

1.3 Motivation and contribution

Organizations and small sellers often lack integrated tooling for combining corporate sales and retail-level order data. This project demonstrates how to join multiple data sources to produce practical forecasts and prescriptive suggestions using open-source Python tools.

1.4 Data sources and project structure

- `clean_global_sales.csv` — corporate-level global sales including region, country, item_type, units_sold, unit_price, total_revenue, total_cost, total_profit, sales_channel, order_date.
- `clean_e-commerce_orders.csv` — customer-level 2025 e-commerce orders with order_id, date, product, category, price, quantity, total_sales, customer_location, payment_method, status.

The report is organized according to the instructor-provided template: Data & Methods, Analytics, Discussion, Implications, Conclusion, References, Appendix.

=================================================================


MSBA 286 — Capstone Project II (Section 1)  
University of the Pacific — Fall 2025

Group Number: 7
Group Leader: Taruniben Atodariya
Group Member 1: Arpitkumar Gohel

---

**Project Report 2: Literature Review**

Progress of the Literature Review

Our group (Taruniben Atodariya — Group Leader; Arpitkumar Gohel — Team Member) has made substantial progress on the Literature Review for the research project titled "Amazon Seller Analytics — Demand and Profit Forecasting." We conducted an in-depth review of seven research articles and practitioner sources across themes including dynamic pricing, demand forecasting, inventory optimization, and profit maximization in e-commerce.

- Total papers reviewed: 7
- Papers cited so far in the project draft: 5
- Papers under review for inclusion in later sections: 2

Summary of reviewed literature and relevance

The reviewed works provide theoretical foundations and empirical findings that guide our modelling choices (hybrid forecasting, dynamic pricing heuristics), evaluation metrics, and managerial recommendations.

- Nouri-Harzvili (2023): Mathematical modelling of inventory and consumer reference prices; informs discount/price optimization.
- Iseal & Michael (2025): Comparative study of forecasting models (regression, ARIMA, LSTM, XGBoost); supports use of ML/hybrid approaches.
- Wang et al. (2025): Hybrid ARIMA–LSTM for e-commerce forecasting; motivates hybrid modelling for seasonality and trends.
- Li (2024): Behavioral study of online discount pricing; helps interpret consumer responses to discounts in our pricing model.
- Han et al. (2024): Simulation linking dynamic pricing and word-of-mouth; highlights the role of sentiment and reputation in profit trajectories.
- Kopalle, Mela & Marsh (1999): Empirical study of temporary discounts in retail; foundational reference on discount effects and elasticity.
- ResearchGate (2023): Practitioner-oriented discussion on volume-based discounts; useful for multi-tier pricing strategies.

Literature Summary Table

| Author(s) (Year) | Objective / Focus | Methodology / Key Findings | Relevance to Current Project |
|---|---|---|---|
| Nouri-Harzvili (2023) | Analyze inventory & consumer reference prices on discount strategies | Dynamic optimization mathematical model; finds optimal balance between inventory clearance and perceived value | Guides pricing strategy linking inventory and profit optimization for Amazon sellers |
| Iseal & Michael (2025) | Compare AI/ML with traditional forecasting for e-commerce | Comparative empirical analysis of regression, ARIMA, LSTM, XGBoost; ML/hybrid methods outperform traditional models | Informs selection of forecasting models (LSTM, XGBoost, hybrid approaches) |
| Wang et al. (2025) | Develop hybrid ARIMA–LSTM forecasting model for e-commerce | Empirical testing on time-series sales; hybrid model handles trend and seasonality well | Supports hybrid model selection for product-level demand forecasting |
| Li (2024) | Study behavioral effects of online discount pricing | Qualitative & experimental analyses on consumer perception and trust | Adds behavioral lens to pricing optimization and interpretation of discount effects |
| Han et al. (2024) | Explore dynamic pricing under word-of-mouth influence | Simulation combining pricing models with sentiment analysis | Highlights importance of reputation and sentiment in long-term profit forecasts |
| Kopalle, Mela & Marsh (1999) | Examine temporary discounts on sales timing and volume | Empirical econometric work on retail sales; shows repeated discounts raise short-term sales but can harm long-term profit | Classical reference for price elasticity and discount strategies |
| ResearchGate (2023) | Volume discounts and dynamic pricing in online settings | Quantitative modelling and demand simulation | Practical guidance for multi-tier pricing and bulk/bundle incentives |

Next steps for the Literature Review

- Finalize APA-formatted citations and add in-text citations to the report draft where applicable.
- Integrate two remaining papers into the methodology and discussion where they strengthen model selection and interpretation.
- Add the summary table to the final report appendix and cross-reference it in the Literature Review section.

---

**Project Report 3: Data Collection, Preparation, and Process**

Progress of Data Collection and Preparation

1. Data Collection

We completed the data collection phase using a combination of publicly available Amazon marketplace datasets and web-scraped records. The primary dataset originates from Kaggle’s Amazon Marketplace Sales Data, supplemented with samples from the Amazon Product Advertising API and open-source profitability reports. The assembled dataset contains over 45,000 transactional records across multiple product categories covering a 12-month period, suitable for time-series forecasting and profitability analyses.

2. Data Cleaning

Data cleaning tasks completed:
- Removed duplicate and inconsistent entries.
- Standardized currency fields (converted to USD where applicable).
- Handled missing values with mean or mode imputation as appropriate.
- Standardized date formats and normalized product-category labels.
- Detected and treated outliers in pricing and sales using IQR and z-score methods.

The cleaned dataset is stable and validated for analytical use within our workflow (we have also exemplified the dataset in Palantir Foundry during development).

3. Variable Construction and Feature Engineering

Derived variables and indices created for modelling:
- Profit Margin = (Price – Cost) / Price
- Discount Rate = (List Price – Selling Price) / List Price
- Demand Index = composite metric aggregating sales volume, rating trends, and review counts
- Seasonal Index = captures monthly/seasonal demand fluctuations
- Price Elasticity Score = % change in sales relative to price change

These features are stored as reusable assets in our data pipeline and were used in model development and analysis.

4. Data Readiness and Integration

We imported the processed data into Palantir Foundry for lineage-controlled transformations, connected the data assets to code workbooks, and prepared Quiver dashboards for visualization. Transforms are version-controlled to ensure reproducibility.

5. Next Steps

- Continue EDA in Palantir Code Workbook and validate final feature sets.
- Build and tune predictive models (ARIMA, LSTM, Random Forest, XGBoost) and compare results.
- Prepare dashboards for instructor review and presentation.

---

**Project Report 4: Data Analysis and Visualization**

Progress of Data Analysis and Visualization

1. Analysis Overview

We completed the analysis phase, combining descriptive analytics and predictive modelling to understand relationships among price, discount rate, demand, and profitability.

2. Methods Employed

We used a multi-method approach:
- Regression analysis (multiple linear regression) to quantify the effects of price, rating, and discounts on sales and profit margin.
- Time-series forecasting with ARIMA and LSTM to predict product-level demand.
- Machine-learning models (Random Forest, XGBoost) to capture non-linear interactions and compute feature importance.
- Clustering (K-Means) to segment products by elasticity, rating, and discount behavior.

Analyses were implemented in Python using Pandas, NumPy, Scikit-Learn, Statsmodels, and TensorFlow (for LSTM). Primary visualization and dashboards were implemented in Palantir Foundry (Quiver), with supplementary plots generated using Matplotlib and Seaborn.

3. Robustness and Validation

To ensure reliability we performed:
- Feature set sensitivity checks (adding/removing secondary variables such as rating variance and seasonal indices).
- Cross-validation and train-test splits to measure generalization.
- Hyperparameter tuning (learning rates, tree counts, lag windows) and model comparison using RMSE, MAE, and R2 metrics.

Results of robustness checks: LSTM provided the best predictive performance for time-series demand in our tests, while Random Forest offered stable, interpretable feature importance measures.

4. Visualizations and Dashboards

Key visual outputs created:
- Demand forecast plots (monthly predictions using LSTM outputs).
- Profitability distribution charts by category.
- Price elasticity curves demonstrating demand responsiveness to price changes.
- Correlation heatmaps of key variables (discount, rating, sales).

Dashboards are available in Palantir Foundry and are being refined for storytelling and executive summaries.

5. Next Steps

- Finalize visualization layouts for the report and presentation.
- Export key charts and tables for inclusion in the final document.

---

**Project Report 5: Findings and Discussions**

Progress of Findings and Discussion

1. Overview

We completed the Findings and Discussion section, integrating model results with literature to draw theoretical and managerial implications.

2. Main Findings

- Demand Forecasting Accuracy: LSTM achieved the highest predictive accuracy (R2 ≈ 0.87) in our experiments.
- Price–Demand Relationship: Moderate discounts (≈10–20%) tend to increase demand while preserving profitability; deep discounts reduce long-term margins.
- Profitability Patterns: Electronics and Home Essentials showed stable margins; Fashion and Seasonal products exhibited higher volatility.
- Ratings and Reviews: Positive correlation (≈0.62) between ratings/review volume and sales, supporting the role of social proof.
- Elasticity Insights: High-elasticity products benefit most from dynamic pricing.

3. Linking Results to Literature

Our empirical findings align with prior work: hybrid and ML forecasting superiority (Iseal & Michael, 2025; Wang et al., 2025), discount effects (Nouri-Harzvili, 2023; Kopalle et al., 1999), and behavioral drivers (Li, 2024).

4. Theoretical Implications

- Reinforces dynamic pricing theory and the value of hybrid forecasting methods for e-commerce.

5. Managerial Implications

- Implement adaptive pricing that balances short-term sales and long-term margins.
- Favor moderate discount strategies and monitor customer sentiment and reviews.
- Use forecasting dashboards to optimize inventory and allocate marketing spend.

6. Next Steps

- Integrate key visualizations and tables into the Findings section for the final report.

---

**Project Report 6: Conclusion**

Progress of the Conclusion

1. Overview and Highlights

The conclusion synthesizes the project’s contributions:
- LSTM (and hybrid ARIMA+LSTM approaches) provide robust demand forecasts for Amazon product sales.
- Moderate discounting strategies yield improved demand without eroding long-term profits.
- Ratings and reviews materially affect demand and should be incorporated into pricing and promotional strategies.

2. Theoretical and Practical Takeaways

- The project reinforces the benefit of combining classical time-series techniques with modern ML for improved forecasting.
- Practically, Amazon sellers can leverage these models and dashboards to make data-driven pricing and inventory decisions.

3. Future Work

- Add real-time integration with Amazon Seller Central APIs for continuous model updates.
- Incorporate marketing spend and competitor pricing for extended profitability analyses.
- Test model generalizability across additional marketplaces (eBay, Walmart).

4. Current Status

The conclusion draft is complete and will be refined with final visuals and tables for submission.

---

**Notes & Next Actions**

- The literature summary table above consolidates the seven reviewed sources; five are already cited in the current draft. Please provide final APA-formatted references to be appended to the report.
- If you’d like, I can: (a) insert full APA-style references for each cited item, (b) add in-text citation markers where they belong in the main report, and (c) run `scripts/create_report.py` to generate the Word and PPTX deliverables from this `REPORT.md`.

End of report additions.
