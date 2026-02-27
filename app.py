import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Executive Financial Dashboard",
    layout="wide"
)

st.title("📊 Executive Financial Intelligence Dashboard")
st.markdown("Strategic revenue, customer and forecasting insights")

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    monthly = pd.read_csv("monthly_revenue.csv")
    customers = pd.read_csv("customer_summary.csv")
    churn = pd.read_csv("churn_summary.csv")
    return monthly, customers, churn

monthly_revenue, customer_summary, churn_summary = load_data()

monthly_revenue['month'] = pd.to_datetime(monthly_revenue['month'])

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.header("🔎 Filters")

min_date = monthly_revenue['month'].min()
max_date = monthly_revenue['month'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

filtered_monthly = monthly_revenue[
    (monthly_revenue['month'] >= pd.to_datetime(date_range[0])) &
    (monthly_revenue['month'] <= pd.to_datetime(date_range[1]))
]

# ==========================================
# KPIs
# ==========================================
total_revenue = customer_summary['revenue'].sum()
total_customers = len(customer_summary)
total_orders = customer_summary['total_orders'].sum()
avg_order_value = total_revenue / total_orders

monthly_series = filtered_monthly.set_index('month')['revenue']

if len(monthly_series) > 1:
    growth_rate = monthly_series.pct_change().mean() * 100
else:
    growth_rate = 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Customers", f"{total_customers:,}")
col3.metric("Orders", f"{total_orders:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")
col5.metric("Avg Monthly Growth", f"{growth_rate:.2f}%")

st.divider()

# ==========================================
# REVENUE TREND (Plotly - Professional)
# ==========================================
st.subheader("📈 Revenue Trend")

fig = px.line(
    filtered_monthly,
    x="month",
    y="revenue",
    markers=True,
    color_discrete_sequence=["#1f3b4d"]
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="Revenue",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================================
# REVENUE DISTRIBUTION
# ==========================================
st.subheader("💰 Customer Revenue Distribution")

fig2 = px.histogram(
    customer_summary,
    x="revenue",
    nbins=40,
    color_discrete_sequence=["#5c4d7d"]
)

fig2.update_layout(template="plotly_white", height=400)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ==========================================
# TOP 10% CONTRIBUTION
# ==========================================
st.subheader("💎 Revenue Concentration")

customer_sorted = customer_summary.sort_values(by="revenue", ascending=False)
top_10 = int(0.1 * len(customer_sorted))
top_revenue = customer_sorted.head(top_10)['revenue'].sum()
percentage = (top_revenue / total_revenue) * 100

st.metric("Top 10% Revenue Contribution", f"{percentage:.2f}%")

st.divider()

# ==========================================
# CHURN ANALYSIS
# ==========================================
st.subheader("🔄 Customer Retention")

fig3 = px.pie(
    churn_summary,
    names="customer_type",
    values="count",
    color_discrete_sequence=["#2f4b7c", "#d45087"]
)

fig3.update_layout(template="plotly_white", height=400)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ==========================================
# FORECAST
# ==========================================
st.subheader("📊 Revenue Forecast (3-Month Moving Avg)")

forecast = monthly_series.rolling(3).mean().reset_index()

fig4 = px.line(filtered_monthly, x="month", y="revenue")
fig4.add_scatter(
    x=forecast['month'],
    y=forecast['revenue'],
    mode='lines',
    name="Forecast",
    line=dict(dash='dash', color='#e4572e')
)

fig4.update_layout(template="plotly_white", height=400)

st.plotly_chart(fig4, use_container_width=True)

if len(forecast.dropna()) > 0:
    st.success(f"📌 Estimated Next Month Revenue: ${forecast['revenue'].iloc[-1]:,.0f}")

st.divider()

# ==========================================
# EXECUTIVE SUMMARY
# ==========================================
st.subheader("📌 Executive Summary")

st.markdown(f"""
• Total revenue generated: **${total_revenue:,.0f}**  
• Average order value: **${avg_order_value:,.2f}**  
• Revenue growth trend: **{growth_rate:.2f}% per month**  
• High revenue concentration in top customers  
• Retention opportunity due to large one-time buyer segment  

This dashboard supports strategic planning, financial forecasting and growth optimization.
""")
