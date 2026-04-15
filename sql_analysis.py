import streamlit as st
import duckdb

st.title(" E-commerce Analytics Dashboard (SQL Powered)")

# Query data using SQL
query = """
SELECT event_type, COUNT(*) AS count
FROM 'data/ecommerce.parquet'
GROUP BY event_type
"""

df = duckdb.query(query).to_df()

st.subheader("Event Distribution")
st.bar_chart(df.set_index('event_type'))
