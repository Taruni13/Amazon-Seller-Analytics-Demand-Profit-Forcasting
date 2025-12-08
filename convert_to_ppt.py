"""Convert Markdown presentation to PowerPoint format."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_presentation():
    """Create PowerPoint presentation from slides data."""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Define colors
    pacific_orange = RGBColor(232, 117, 0)  # #E87500
    pacific_dark = RGBColor(17, 17, 17)      # #111111
    
    # Slide 1: Title Slide
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    title_box = slide1.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.text = "Amazon Seller Analytics"
    title_p = title_frame.paragraphs[0]
    title_p.font.size = Pt(44)
    title_p.font.bold = True
    title_p.font.color.rgb = pacific_orange
    title_p.alignment = PP_ALIGN.CENTER
    
    subtitle_box = slide1.shapes.add_textbox(Inches(0.5), Inches(3.5), Inches(9), Inches(0.8))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "Demand and Profit Forecasting Dashboard"
    subtitle_p = subtitle_frame.paragraphs[0]
    subtitle_p.font.size = Pt(32)
    subtitle_p.font.color.rgb = pacific_dark
    subtitle_p.alignment = PP_ALIGN.CENTER
    
    info_box = slide1.shapes.add_textbox(Inches(1), Inches(5.5), Inches(8), Inches(1.5))
    info_frame = info_box.text_frame
    info_frame.text = "MSBA 286 — Capstone Project II\nUniversity of the Pacific — Fall 2025\n\nGroup 7: Taruniben Atodariya • Arpitkumar Gohel"
    for p in info_frame.paragraphs:
        p.font.size = Pt(16)
        p.alignment = PP_ALIGN.CENTER
    
    # Slide 2: Project Overview
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    title2 = slide2.shapes.title
    title2.text = "Project Overview"
    title2.text_frame.paragraphs[0].font.color.rgb = pacific_orange
    
    content2 = slide2.placeholders[1].text_frame
    content2.text = "What We Built\nEnd-to-end interactive analytics dashboard for Amazon sellers"
    p = content2.add_paragraph()
    p.text = "\nKey Features"
    p.font.bold = True
    content2.add_paragraph().text = "✅ Exploratory Data Analysis (EDA)"
    content2.add_paragraph().text = "✅ Machine Learning Predictive Modeling"
    content2.add_paragraph().text = "✅ Time-Series Forecasting"
    content2.add_paragraph().text = "✅ Actionable Business Recommendations"
    p = content2.add_paragraph()
    p.text = "\nData Scale"
    p.font.bold = True
    content2.add_paragraph().text = "• 45,000+ transactional records"
    content2.add_paragraph().text = "• 2 comprehensive datasets"
    content2.add_paragraph().text = "• 12-month time period coverage"
    
    # Slide 3: Problem Statement
    slide3 = prs.slides.add_slide(prs.slide_layouts[1])
    title3 = slide3.shapes.title
    title3.text = "Problem Statement & Objectives"
    title3.text_frame.paragraphs[0].font.color.rgb = pacific_orange
    
    content3 = slide3.placeholders[1].text_frame
    p = content3.paragraphs[0]
    p.text = "Critical Business Questions"
    p.font.bold = True
    p.font.size = Pt(20)
    content3.add_paragraph().text = "1. Which products and regions generate the most revenue and profit?"
    content3.add_paragraph().text = "2. Can we reliably forecast demand and profit for 3-6 months?"
    content3.add_paragraph().text = "3. Which features (price, channel, category) most influence revenue?"
    p = content3.add_paragraph()
    p.text = "\nSolution Approach"
    p.font.bold = True
    p.font.size = Pt(20)
    content3.add_paragraph().text = "• Integrate multiple data sources"
    content3.add_paragraph().text = "• Apply ML and time-series forecasting"
    content3.add_paragraph().text = "• Deliver interactive dashboard with insights"
    
    # Slide 4: Data Sources
    slide4 = prs.slides.add_slide(prs.slide_layouts[1])
    title4 = slide4.shapes.title
    title4.text = "Data Sources & Preparation"
    title4.text_frame.paragraphs[0].font.color.rgb = pacific_orange
    
    content4 = slide4.placeholders[1].text_frame
    p = content4.paragraphs[0]
    p.text = "Datasets"
    p.font.bold = True
    content4.add_paragraph().text = "Global Sales (45,000+ records): Region, Country, Item Type, Sales Channel, Units, Revenue, Cost, Profit"
    content4.add_paragraph().text = "E-Commerce Orders (2025 records): Product, Category, Price, Quantity, Customer Location, Payment Method"
    p = content4.add_paragraph()
    p.text = "\nFeature Engineering"
    p.font.bold = True
    content4.add_paragraph().text = "• Profit Margin = (Price - Cost) / Price"
    content4.add_paragraph().text = "• Demand Index = Sales Volume + Ratings + Reviews"
    content4.add_paragraph().text = "• Price Elasticity = % Sales Change / % Price Change"
    
    # Slide 5: Methodology
    slide5 = prs.slides.add_slide(prs.slide_layouts[1])
    title5 = slide5.shapes.title
    title5.text = "Methodology & Models"
    title5.text_frame.paragraphs[0].font.color.rgb = pacific_orange
    
    content5 = slide5.placeholders[1].text_frame
    p = content5.paragraphs[0]
    p.text = "Three-Pronged Approach"
    p.font.bold = True
    p.font.size = Pt(22)
    
    p = content5.add_paragraph()
    p.text = "\n1. Exploratory Data Analysis"
    p.font.bold = True
    content5.add_paragraph().text = "   Descriptive statistics, time-series trends, rankings"
    
    p = content5.add_paragraph()
    p.text = "\n2. Predictive Modeling (Supervised ML)"
    p.font.bold = True
    content5.add_paragraph().text = "   • Random Forest (R² ≈ 0.85-0.87)"
    content5.add_paragraph().text = "   • Gradient Boosting, Linear Regression"
    
    p = content5.add_paragraph()
    p.text = "\n3. Time-Series Forecasting"
    p.font.bold = True
    content5.add_paragraph().text = "   • ARIMA (R² ≈ 0.78-0.82)"
    content5.add_paragraph().text = "   • Hybrid ARIMA-LSTM (R² ≈ 0.87)"
    
    # Slide 6: Dashboard Features
    slide6 = prs.slides.add_slide(prs.slide_layouts[1])
    title6 = slide6.shapes.title
    title6.text = "Dashboard Features"
    title6.text_frame.paragraphs[0].font.color.rgb = pacific_orange
    
    content6 = slide6.placeholders[1].text_frame
    p = content6.paragraphs[0]
    p.text = "6 Interactive Pages"
    p.font.bold = True
    p.font.size = Pt(22)
    content6.add_paragraph().text = "• Home: Overview and navigation"
    content6.add_paragraph().text = "• EDA: Data exploration and visualization"
    content6.add_paragraph().text = "• Analytics: ML model training and comparison"
    content6.add_paragraph().text = "• Forecasting: 3-6 month predictions"
    content6.add_paragraph().text = "• Insights: Aggregated KPIs and findings"
    content6.add_paragraph().text = "• Suggestions: User feedback collection"
    p = content6.add_paragraph()
    p.text = "\nTech Stack: Streamlit, Python 3.11, Scikit-learn, Statsmodels"
    p.font.size = Pt(14)
    p.font.italic = True
    
    # Slide 7: Key Findings
    slide7 = prs.slides.add_slide(prs.slide_layouts[1])
    title7 = slide7.shapes.title
    title7.text = "Key Findings"
    title7.text_frame.paragraphs[0].font.color.rgb = pacific_orange
    
    content7 = slide7.placeholders[1].text_frame
    p = content7.paragraphs[0]
    p.text = "1. Forecasting Performance"
    p.font.bold = True
    content7.add_paragraph().text = "   LSTM: R² = 0.87 (highest accuracy)"
    content7.add_paragraph().text = "   Reliable 3-6 month forecasts"
    
    p = content7.add_paragraph()
    p.text = "\n2. Optimal Pricing Strategy"
    p.font.bold = True
    content7.add_paragraph().text = "   10-20% discounts preserve profit"
    content7.add_paragraph().text = "   Deep discounts (>30%) harm margins"
    
    p = content7.add_paragraph()
    p.text = "\n3. Social Proof Impact"
    p.font.bold = True
    content7.add_paragraph().text = "   r = 0.62 correlation (ratings ↔ sales)"
    
    p = content7.add_paragraph()
    p.text = "\n4. Category Performance"
    p.font.bold = True
    content7.add_paragraph().text = "   Electronics & Home: Stable margins"
    content7.add_paragraph().text = "   Fashion: Dynamic pricing opportunity"
    
    # Slide 8: Business Recommendations
    slide8 = prs.slides.add_slide(prs.slide_layouts[1])
    title8 = slide8.shapes.title
    title8.text = "Business Recommendations"
    title8.text_frame.paragraphs[0].font.color.rgb = pacific_orange
    
    content8 = slide8.placeholders[1].text_frame
    p = content8.paragraphs[0]
    p.text = "Pricing Strategy"
    p.font.bold = True
    content8.add_paragraph().text = "✅ Implement dynamic pricing using ML models"
    content8.add_paragraph().text = "✅ Target 10-20% discount range"
    content8.add_paragraph().text = "✅ Category-specific pricing"
    
    p = content8.add_paragraph()
    p.text = "\nInventory Management"
    p.font.bold = True
    content8.add_paragraph().text = "✅ Use 3-6 month forecasts for planning"
    content8.add_paragraph().text = "✅ Maintain safety stock by volatility"
    content8.add_paragraph().text = "✅ Prioritize high-margin items"
    
    p = content8.add_paragraph()
    p.text = "\nMarketing"
    p.font.bold = True
    content8.add_paragraph().text = "✅ Solicit product reviews actively"
    content8.add_paragraph().text = "✅ Balance online/offline channels"
    
    # Slide 9: Technical Architecture
    slide9 = prs.slides.add_slide(prs.slide_layouts[1])
    title9 = slide9.shapes.title
    title9.text = "Technical Architecture"
    title9.text_frame.paragraphs[0].font.color.rgb = pacific_orange
    
    content9 = slide9.placeholders[1].text_frame
    p = content9.paragraphs[0]
    p.text = "Project Structure"
    p.font.bold = True
    content9.add_paragraph().text = "App.py — Dashboard entry"
    content9.add_paragraph().text = "pages/ — 1_EDA, 2_Analytics, 3_Forecasting,"
    content9.add_paragraph().text = "         4_Insights, 5_Suggestion"
    content9.add_paragraph().text = "src/ — eda.py, ml.py, theme.py"
    content9.add_paragraph().text = "data_process/ — clean_global_sales.csv,"
    content9.add_paragraph().text = "                clean_e-commerce_orders.csv"
    p = content9.add_paragraph()
    p.text = "\nDeployment: Streamlit Community Cloud"
    p.font.bold = True
    content9.add_paragraph().text = "Repo: github.com/Taruni13/Amazon-Seller-Analytics"
    
    # Slide 10: Results & Thank You
    slide10 = prs.slides.add_slide(prs.slide_layouts[1])
    title10 = slide10.shapes.title
    title10.text = "Results & Impact"
    title10.text_frame.paragraphs[0].font.color.rgb = pacific_orange
    
    content10 = slide10.placeholders[1].text_frame
    p = content10.paragraphs[0]
    p.text = "Quantitative Outcomes"
    p.font.bold = True
    content10.add_paragraph().text = "• Revenue forecast error: < 15% MAE"
    content10.add_paragraph().text = "• Demand prediction: R² = 0.87"
    content10.add_paragraph().text = "• Profit margin prediction: R² = 0.82"
    
    p = content10.add_paragraph()
    p.text = "\nBusiness Impact"
    p.font.bold = True
    content10.add_paragraph().text = "• Identified 20% of products → 80% of profit"
    content10.add_paragraph().text = "• Optimal discount range: 10-20%"
    content10.add_paragraph().text = "• Rating impact quantified: +62% correlation"
    
    p = content10.add_paragraph()
    p.text = "\n\nThank You! Questions?"
    p.font.bold = True
    p.font.size = Pt(24)
    p.font.color.rgb = pacific_orange
    
    # Save presentation
    output_path = "Amazon_Seller_Analytics_Presentation.pptx"
    prs.save(output_path)
    print(f"✅ PowerPoint presentation created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_presentation()
