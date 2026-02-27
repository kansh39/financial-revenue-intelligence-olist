import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Executive Financial Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Executive Financial Intelligence Dashboard")
st.markdown("Advanced revenue, customer, and forecasting analytics for strategic decision-making.")

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    monthly = pd.read_csv("monthly_revenue.csv")
    customers = pd.read_csv("customer_summary.csv")
    churn = pd.read_csv("churn_summary.csv")
    return monthly, customers, churn

monthly_revenue, customer_summary, churn_summary = load_data()

monthly_revenue['month'] = pd.to_datetime(monthly_revenue['month'])

# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.header("🔎 Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    monthly_revenue['month'].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    monthly_revenue['month'].max()
)

filtered_monthly = monthly_revenue[
    (monthly_revenue['month'] >= pd.to_datetime(start_date)) &
    (monthly_revenue['month'] <= pd.to_datetime(end_date))
]

customer_type_filter = st.sidebar.selectbox(
    "Customer Type",
    ["All", "Repeat", "One-Time"]
)

if customer_type_filter != "All":
    filtered_customers = customer_summary[
        customer_summary['total_orders'].apply(
            lambda x: "Repeat" if x > 1 else "One-Time"
        ) == customer_type_filter
    ]
else:
    filtered_customers = customer_summary

# =====================================================
# KPI SECTION
# =====================================================
total_revenue = filtered_customers['revenue'].sum()
total_customers = filtered_customers.shape[0]
total_orders = filtered_customers['total_orders'].sum()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

# Revenue growth
monthly_series = filtered_monthly.set_index('month')['revenue']
growth_rate = monthly_series.pct_change().mean() * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Customers", f"{total_customers:,}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")
col5.metric("Avg Monthly Growth", f"{growth_rate:.2f}%")

st.markdown("---")

# =====================================================
# REVENUE TREND
# =====================================================
st.subheader("📈 Revenue Trend")

fig1, ax1 = plt.subplots(figsize=(14,4))
sns.lineplot(
    data=filtered_monthly,
    x='month',
    y='revenue',
    ax=ax1,
    linewidth=3,
    color="#003f5c"
)
plt.xticks(rotation=45)
plt.title("Monthly Revenue Performance")
st.pyplot(fig1)

st.markdown("---")

# =====================================================
# REVENUE DISTRIBUTION
# =====================================================
st.subheader("💰 Revenue Distribution Across Customers")

fig2, ax2 = plt.subplots(figsize=(8,4))
sns.histplot(filtered_customers['revenue'], bins=50, color="#58508d")
plt.title("Customer Revenue Distribution")
st.pyplot(fig2)

st.markdown("---")

# =====================================================
# TOP 10% REVENUE CONTRIBUTION
# =====================================================
st.subheader("💎 Revenue Concentration (Top 10%)")

customer_sorted = filtered_customers.sort_values(by='revenue', ascending=False)
top_10_percent = int(0.1 * len(customer_sorted))

if top_10_percent > 0:
    top_revenue = customer_sorted.head(top_10_percent)['revenue'].sum()
    percentage = (top_revenue / total_revenue) * 100
else:
    percentage = 0

st.metric("Top 10% Revenue Contribution", f"{percentage:.2f}%")

st.markdown("---")

# =====================================================
# CHURN / RETENTION
# =====================================================
st.subheader("🔄 Customer Retention Overview")

fig3, ax3 = plt.subplots()
colors = ["#2f4b7c", "#d45087"]

ax3.pie(
    churn_summary['count'],
    labels=churn_summary['customer_type'],
    autopct='%1.1f%%',
    colors=colors
)
plt.title("Repeat vs One-Time Customers")
st.pyplot(fig3)

st.markdown("---")

# =====================================================
# FORECASTING
# =====================================================
st.subheader("📊 Revenue Forecast (3-Month Moving Average)")

forecast = monthly_series.rolling(window=3).mean()

fig4, ax4 = plt.subplots(figsize=(14,4))
plt.plot(monthly_series, label="Actual", linewidth=3, color="#003f5c")
plt.plot(forecast, label="Forecast", linestyle="--", linewidth=3, color="#ff6361")
plt.legend()
plt.xticks(rotation=45)
plt.title("Revenue Forecasting")
st.pyplot(fig4)

if len(forecast.dropna()) > 0:
    next_forecast = forecast.iloc[-1]
    st.success(f"📌 Estimated Next Month Revenue: ${next_forecast:,.0f}")

st.markdown("---")

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================
st.subheader("📌 Executive Summary")

st.markdown(f"""
- Revenue in selected period: **${total_revenue:,.0f}**
- Average monthly growth rate: **{growth_rate:.2f}%**
- Top 10% customers contribute **{percentage:.2f}%** of revenue.
- Retention opportunity exists due to high one-time purchase ratio.
- Forecast indicates stable revenue trajectory.

This dashboard enables strategic decisions in:
- Revenue planning  
- Customer retention  
- Marketing optimization  
- Financial forecasting  
""")
