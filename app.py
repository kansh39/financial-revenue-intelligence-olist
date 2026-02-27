import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Financial Revenue Intelligence",
    layout="wide"
)

st.title("📊 Financial & Revenue Intelligence Dashboard")
st.markdown("Executive-level analytics for revenue, churn and profitability insights.")

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    monthly = pd.read_csv("monthly_revenue.csv")
    customers = pd.read_csv("customer_summary.csv")
    churn = pd.read_csv("churn_summary.csv")
    return monthly, customers, churn

monthly_revenue, customer_summary, churn_summary = load_data()

# ==============================
# KPI SECTION
# ==============================
total_revenue = customer_summary['revenue'].sum()
total_customers = customer_summary.shape[0]
total_orders = customer_summary['total_orders'].sum()
avg_order_value = total_revenue / total_orders

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Customers", f"{total_customers:,}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")

# ==============================
# REVENUE TREND
# ==============================
st.subheader("📈 Monthly Revenue Trend")

monthly_revenue['month'] = pd.to_datetime(monthly_revenue['month'])

fig1, ax1 = plt.subplots(figsize=(12,4))
sns.lineplot(data=monthly_revenue, x='month', y='revenue', ax=ax1, color="#1f77b4")
plt.xticks(rotation=45)
plt.title("Revenue Over Time")
st.pyplot(fig1)

st.markdown("---")

# ==============================
# TOP CUSTOMER CONTRIBUTION
# ==============================
st.subheader("💎 Top 10% Customers Revenue Contribution")

customer_sorted = customer_summary.sort_values(by='revenue', ascending=False)

top_10_percent = int(0.1 * len(customer_sorted))
top_revenue = customer_sorted.head(top_10_percent)['revenue'].sum()
percentage = (top_revenue / total_revenue) * 100

st.metric("Top 10% Revenue Contribution", f"{percentage:.2f}%")

st.markdown("---")

# ==============================
# CHURN ANALYSIS
# ==============================
st.subheader("🔄 Customer Retention Analysis")

fig2, ax2 = plt.subplots()
colors = ["#2ca02c", "#d62728"]

ax2.pie(
    churn_summary['count'],
    labels=churn_summary['customer_type'],
    autopct='%1.1f%%',
    colors=colors
)

plt.title("Repeat vs One-Time Customers")
st.pyplot(fig2)

st.markdown("---")

# ==============================
# FORECASTING SECTION
# ==============================
st.subheader("📊 Revenue Forecast (Moving Average - 3 Months)")

monthly_series = monthly_revenue.set_index('month')['revenue']
forecast = monthly_series.rolling(window=3).mean()

fig3, ax3 = plt.subplots(figsize=(12,4))
plt.plot(monthly_series, label="Actual Revenue", color="#1f77b4")
plt.plot(forecast, label="Forecast (Moving Avg)", color="#ff7f0e")
plt.legend()
plt.xticks(rotation=45)
plt.title("Revenue Forecast")
st.pyplot(fig3)

next_forecast = forecast.iloc[-1]
st.success(f"📌 Estimated Next Month Revenue: ${next_forecast:,.0f}")

st.markdown("---")

# ==============================
# BUSINESS INSIGHTS
# ==============================
st.subheader("📌 Business Insights")

st.markdown("""
- Revenue shows consistent growth trend over time.
- A small group of high-value customers drives significant revenue.
- Majority of customers are one-time buyers → retention opportunity.
- Forecast suggests stable revenue continuation.

This dashboard supports financial planning, marketing optimization, and growth strategy.
""")
