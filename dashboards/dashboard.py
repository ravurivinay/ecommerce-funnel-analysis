import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 E-commerce Funnel Analytics Dashboard")

# -------------------------
# KPI QUERIES (NO FULL LOAD)
# -------------------------

# Event counts
event_query = """
SELECT event_type, COUNT(*) AS count
FROM 'data/ecommerce.parquet'
GROUP BY event_type
"""

event_df = duckdb.query(event_query).to_df()

# Conversion rate
conv_query = """
SELECT 
    COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) * 100.0 /
    COUNT(CASE WHEN event_type = 'view' THEN 1 END) AS conversion_rate
FROM 'data/ecommerce.parquet'
"""

conversion_rate = duckdb.query(conv_query).to_df().iloc[0,0]

# Revenue
revenue_query = """
SELECT SUM(price) AS revenue
FROM 'data/ecommerce.parquet'
WHERE event_type = 'purchase'
"""

revenue = duckdb.query(revenue_query).to_df().iloc[0,0]

# -------------------------
# KPI DISPLAY
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Events", f"{event_df['count'].sum():,}")
col2.metric("Conversion Rate", f"{conversion_rate:.2f}%")
col3.metric("Revenue", f"${revenue:,.0f}")

# -------------------------
# EVENT DISTRIBUTION
# -------------------------
st.subheader("📊 Event Distribution")
st.bar_chart(event_df.set_index('event_type'))

# -------------------------
# FUNNEL
# -------------------------
st.subheader("🔻 Funnel")

funnel_df = event_df.copy()
funnel_df.columns = ["Stage", "Count"]
st.bar_chart(funnel_df.set_index("Stage"))

# -------------------------
# TOP BRANDS (LIMITED)
# -------------------------
brand_query = """
SELECT brand, COUNT(*) AS count
FROM 'data/ecommerce.parquet'
GROUP BY brand
ORDER BY count DESC
LIMIT 10
"""

brand_df = duckdb.query(brand_query).to_df()

st.subheader("🏆 Top Brands")
st.bar_chart(brand_df.set_index('brand'))

# -------------------------
# PRICE SAMPLE (LIMITED)
# -------------------------
price_query = """
SELECT price
FROM 'data/ecommerce.parquet'
LIMIT 5000
"""

price_df = duckdb.query(price_query).to_df()

st.subheader("💰 Price Trend (Sample)")
st.line_chart(price_df)