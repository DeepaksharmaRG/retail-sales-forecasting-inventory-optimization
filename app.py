# -----------------------------
# IMPORT FIX (VERY IMPORTANT)
# -----------------------------
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -----------------------------
# LIBRARIES
# -----------------------------
import streamlit as st
import pandas as pd
import plotly.express as px

from src.pipeline import run_pipeline
from src.kpi import calculate_kpis
from src.inventory import calculate_inventory

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="RetailIQ Dashboard",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📊 RetailIQ")
st.sidebar.caption("Forecasting • Inventory • Insights")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Sales Analysis",
        "Demand Forecasting",
        "Inventory Optimization"
    ]
)

# -----------------------------
# DATA LOAD (PIPELINE)
# -----------------------------
num_days = st.sidebar.slider("Data Size (Days)", 200, 1000, 365)

df, test_df, mae, rmse = run_pipeline(num_days)

# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.subheader("Filters")

category = st.sidebar.multiselect(
    "Category",
    df['category'].unique(),
    default=list(df['category'].unique())
)

store = st.sidebar.multiselect(
    "Store",
    df['store'].unique(),
    default=list(df['store'].unique())
)

region = st.sidebar.multiselect(
    "Region",
    df['region'].unique(),
    default=list(df['region'].unique())
)

df_filtered = df[
    (df['category'].isin(category)) &
    (df['store'].isin(store)) &
    (df['region'].isin(region))
]

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
if page == "Dashboard":

    st.title("📊 Retail Sales Forecasting & Inventory Optimization Dashboard")

    kpis = calculate_kpis(df_filtered)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Revenue", f"₹ {kpis['revenue']:.2f}")
    col2.metric("📦 Units Sold", f"{kpis['units']}")
    col3.metric("📈 Avg Demand", f"{kpis['avg']:.2f}")
    col4.metric("⚠️ Reorder Alerts", "20")

    st.markdown("### 📉 Daily Revenue Trend")

    trend = df_filtered.groupby("date")['sales'].sum().reset_index()

    fig = px.line(trend, x="date", y="sales")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Category-wise Sales")

    cat = df_filtered.groupby("category")['sales'].sum().reset_index()

    fig2 = px.bar(cat, x="category", y="sales", color="category")
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# SALES ANALYSIS
# -----------------------------
elif page == "Sales Analysis":

    st.title("📊 Sales Performance Analysis")

    df_filtered['month'] = df_filtered['date'].dt.month

    fig = px.line(
        df_filtered,
        x="month",
        y="sales",
        color="category"
    )
    st.plotly_chart(fig, use_container_width=True)

    region_sales = df_filtered.groupby("region")['sales'].sum().reset_index()

    fig2 = px.bar(region_sales, x="region", y="sales", color="region")
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# DEMAND FORECASTING
# -----------------------------
elif page == "Demand Forecasting":

    st.title("📈 Demand Forecasting Engine")

    col1, col2, col3 = st.columns(3)

    col1.metric("Model MAE", f"{mae:.2f}")
    col2.metric("Model RMSE", f"{rmse:.2f}")
    col3.metric("Forecast Rows", f"{len(test_df)}")

    st.markdown("### 📉 Actual vs Forecast")

    fig = px.line(
        test_df,
        x="date",
        y=["sales", "forecast"]
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📄 Forecast Table")
    st.dataframe(test_df[['date', 'sales', 'forecast']].tail(30))

# -----------------------------
# INVENTORY OPTIMIZATION
# -----------------------------
elif page == "Inventory Optimization":

    st.title("📦 Inventory Optimization Control Room")

    inventory_df = calculate_inventory(test_df.copy())

    critical = (inventory_df['status'] == "Critical Low").sum()
    total = len(inventory_df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", total)
    col2.metric("Critical Low", critical)
    col3.metric("Safe Stock", total - critical)
    col4.metric("Reorder Needed", critical)

    st.markdown("### 📋 Inventory Table")

    st.dataframe(inventory_df.tail(30))

    st.markdown("### 📊 Inventory Status Distribution")

    status_count = inventory_df['status'].value_counts().reset_index()
    status_count.columns = ['status', 'count']

    fig = px.bar(
        status_count,
        x="status",
        y="count",
        color="status"
    )

    st.plotly_chart(fig, use_container_width=True)