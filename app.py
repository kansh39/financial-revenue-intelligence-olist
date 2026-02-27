import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Olist Revenue Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  — clean professional look
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .main { background-color: #f8f9fa; }

    /* KPI card style */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #2196F3;
    }
    .kpi-label {
        font-size: 13px;
        color: #666;
        font-weight: 500;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 22px;
        font-weight: 700;
        color: #1a1a2e;
    }
    .kpi-sub {
        font-size: 11px;
        color: #999;
        margin-top: 4px;
    }

    /* Section headers */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #1a1a2e;
        margin: 8px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #e0e0e0;
    }

    /* Sidebar */
    .css-1d391kg { background-color: #1a1a2e; }

    /* Hide default streamlit header */
    header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_all_data():
    monthly     = pd.read_csv("monthly_revenue.csv",  parse_dates=["date"])
    customer    = pd.read_csv("customer_revenue.csv")
    repeat      = pd.read_csv("customer_repeat.csv")
    category    = pd.read_csv("category_revenue.csv")
    kpi         = pd.read_csv("kpi_summary.csv")
    return monthly, customer, repeat, category, kpi

try:
    monthly_revenue, customer_revenue, repeat_df, category_rev, kpi_df = load_all_data()
    data_loaded = True
except FileNotFoundError as e:
    data_loaded = False
    missing_file = str(e)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Olist Dashboard")
    st.markdown("**Brazilian E-Commerce**")
    st.markdown("---")

    if data_loaded:
        st.markdown("### 🗂️ Navigation")
        page = st.radio(
            "",
            ["🏠 Overview", "📈 Revenue Trends", "🔮 Forecast",
             "👥 Customers", "💰 Categories"],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("### 📅 Date Range")
        min_date = monthly_revenue['date'].min()
        max_date = monthly_revenue['date'].max()
        st.info(f"**From:** {min_date.strftime('%b %Y')}\n\n**To:** {max_date.strftime('%b %Y')}")

        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        - **Dataset:** Olist (Kaggle)
        - **Rows:** 100K+ orders
        - **Period:** 2016–2018
        - **Built with:** Python + Streamlit
        """)
    else:
        page = "🏠 Overview"

# ─────────────────────────────────────────────
#  ERROR STATE — files not found
# ─────────────────────────────────────────────
if not data_loaded:
    st.error("⚠️ CSV files not found. Please make sure these files are in the same folder as app.py:")
    st.code("""
monthly_revenue.csv
customer_revenue.csv
customer_repeat.csv
category_revenue.csv
kpi_summary.csv
    """)
    st.info("Run the Google Colab notebook first to generate these files, then upload them to the same folder as app.py.")
    st.stop()

# ─────────────────────────────────────────────
#  HELPER: extract KPI values
# ─────────────────────────────────────────────
def get_kpi(metric_name):
    row = kpi_df[kpi_df['Metric'] == metric_name]
    return float(row['Value'].values[0]) if len(row) else 0.0

total_revenue   = get_kpi('Total Revenue')
total_orders    = get_kpi('Total Orders')
total_customers = get_kpi('Unique Customers')
avg_order_value = get_kpi('Avg Order Value')
repeat_pct      = get_kpi('Repeat Customer Rate %')
mom_growth      = get_kpi('MoM Growth %')

# ─────────────────────────────────────────────
#  PAGE: OVERVIEW
# ─────────────────────────────────────────────
if page == "🏠 Overview":
    st.markdown("# 📊 Financial & Revenue Intelligence Dashboard")
    st.markdown("**Dataset:** Brazilian E-Commerce | Olist | Kaggle &nbsp;|&nbsp; **Built for:** Data Analytics Portfolio")
    st.markdown("---")

    # ── KPI CARDS ────────────────────────────────
    st.markdown('<p class="section-header">🎯 Executive KPIs</p>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    kpi_data = [
        (c1, "💰 Total Revenue",    f"BRL {total_revenue:,.0f}",    "All delivered orders"),
        (c2, "📦 Total Orders",     f"{int(total_orders):,}",       "Delivered orders only"),
        (c3, "👥 Customers",        f"{int(total_customers):,}",    "Unique buyers"),
        (c4, "🛒 Avg Order Value",  f"BRL {avg_order_value:,.2f}", "Per order"),
        (c5, "🔁 Repeat Rate",      f"{repeat_pct:.1f}%",          "Bought 2+ times"),
        (c6, "📈 MoM Growth",
             f"{'▲' if mom_growth >= 0 else '▼'} {abs(mom_growth):.1f}%",
             "Last month vs prior"),
    ]

    for col, label, value, sub in kpi_data:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── REVENUE TREND (mini) ──────────────────────
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<p class="section-header">📈 Revenue Trend</p>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.fill_between(monthly_revenue['date'], monthly_revenue['revenue'],
                        alpha=0.15, color='#2196F3')
        ax.plot(monthly_revenue['date'], monthly_revenue['revenue'],
                color='#2196F3', linewidth=2.5, marker='o', markersize=4)
        ax.set_ylabel("Revenue (BRL)", fontsize=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
        ax.grid(axis='y', alpha=0.3)
        ax.spines[['top','right','left']].set_visible(False)
        plt.xticks(rotation=45, fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_right:
        st.markdown('<p class="section-header">🔁 Customer Types</p>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        ax2.pie(
            repeat_df['Count'],
            labels=repeat_df['Type'],
            autopct='%1.1f%%',
            colors=['#2196F3', '#FF9800'],
            startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # ── TOP CATEGORIES (mini) ─────────────────────
    st.markdown('<p class="section-header">💰 Top 5 Categories by Revenue</p>', unsafe_allow_html=True)
    top5 = category_rev.head(5)
    fig3, ax3 = plt.subplots(figsize=(12, 2.5))
    colors = ['#2196F3', '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB']
    bars = ax3.barh(top5['category'][::-1], top5['revenue'][::-1], color=colors[::-1])
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'BRL {x/1e6:.1f}M'))
    ax3.spines[['top','right','left']].set_visible(False)
    ax3.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

# ─────────────────────────────────────────────
#  PAGE: REVENUE TRENDS
# ─────────────────────────────────────────────
elif page == "📈 Revenue Trends":
    st.markdown("# 📈 Revenue Trend Analysis")
    st.markdown("---")

    # Full revenue trend
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.fill_between(monthly_revenue['date'], monthly_revenue['revenue'], alpha=0.1, color='#2196F3')
    ax.plot(monthly_revenue['date'], monthly_revenue['revenue'],
            color='#2196F3', linewidth=2.5, marker='o', markersize=5, label='Monthly Revenue')

    # Annotate peak
    peak_idx  = monthly_revenue['revenue'].idxmax()
    peak_date = monthly_revenue.loc[peak_idx, 'date']
    peak_val  = monthly_revenue.loc[peak_idx, 'revenue']
    ax.annotate(f"Peak\nBRL {peak_val:,.0f}",
                xy=(peak_date, peak_val),
                xytext=(peak_date, peak_val * 0.82),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=9, color='red', ha='center')

    ax.set_title("Monthly Revenue — Olist E-Commerce (2016–2018)", fontsize=14, fontweight='bold')
    ax.set_ylabel("Revenue (BRL)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
    ax.grid(alpha=0.3)
    ax.spines[['top','right']].set_visible(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Stats table
    st.markdown("### 📋 Monthly Revenue Table")
    display_df = monthly_revenue.copy()
    display_df['date'] = display_df['date'].dt.strftime('%Y-%m')
    display_df['revenue'] = display_df['revenue'].map('BRL {:,.2f}'.format)
    display_df.columns = ['Month', 'Revenue']
    st.dataframe(display_df, use_container_width=True, height=400)

# ─────────────────────────────────────────────
#  PAGE: FORECAST
# ─────────────────────────────────────────────
elif page == "🔮 Forecast":
    st.markdown("# 🔮 Revenue Forecasting")
    st.markdown("Using **Moving Average** method — smooths short-term noise to reveal trend direction.")
    st.markdown("---")

    monthly_series = monthly_revenue.set_index('date')['revenue']

    col1, col2 = st.columns([3, 1])
    with col2:
        window = st.selectbox("Moving Average Window", [3, 6, 9], index=0)
        st.markdown("---")
        last_avg = monthly_series.tail(window).mean()
        st.metric("Forecast (Next Month)", f"BRL {last_avg:,.0f}")
        st.metric("Forecast (Avg 3 Months)", f"BRL {last_avg:,.0f}")

    # Build MAs and forecast
    ma = monthly_series.rolling(window=window).mean()
    last_date    = monthly_series.index[-1]
    future_dates = pd.date_range(last_date + pd.DateOffset(months=1), periods=3, freq='MS')
    forecast_s   = pd.Series([last_avg] * 3, index=future_dates)

    with col1:
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(monthly_series.index, monthly_series.values,
                label='Actual Revenue', color='#2196F3', linewidth=2.5, marker='o', markersize=4)
        ax.plot(ma.index, ma.values,
                label=f'{window}-Month Moving Avg', color='#FF9800', linewidth=2, linestyle='--')
        ax.plot(forecast_s.index, forecast_s.values,
                label='Forecast (Next 3 Months)', color='#F44336',
                linewidth=2.5, linestyle='--', marker='D', markersize=9)
        ax.axvspan(forecast_s.index[0], forecast_s.index[-1], alpha=0.1, color='red')
        ax.set_ylabel("Revenue (BRL)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        ax.spines[['top', 'right']].set_visible(False)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("### 📅 3-Month Forecast Values")
    forecast_table = pd.DataFrame({
        'Month'            : [d.strftime('%Y-%m') for d in future_dates],
        'Forecasted Revenue': [f"BRL {last_avg:,.2f}"] * 3,
        'Method'           : [f'{window}-Month Moving Average'] * 3
    })
    st.dataframe(forecast_table, use_container_width=True)

    st.info("💡 **Interview note:** Moving Average is a baseline method. For production, use **Facebook Prophet** or **ARIMA** for seasonality-aware forecasting with confidence intervals.")

# ─────────────────────────────────────────────
#  PAGE: CUSTOMERS
# ─────────────────────────────────────────────
elif page == "👥 Customers":
    st.markdown("# 👥 Customer Segmentation")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    repeat_count   = repeat_df[repeat_df['Type'] == 'Repeat']['Count'].values[0]
    onetime_count  = repeat_df[repeat_df['Type'] == 'One-Time']['Count'].values[0]
    total_cust     = repeat_count + onetime_count

    with col1:
        st.metric("Total Unique Customers", f"{total_cust:,}")
    with col2:
        st.metric("Repeat Customers", f"{repeat_count:,}",
                  delta=f"{repeat_count/total_cust*100:.1f}% of total")
    with col3:
        st.metric("One-Time Customers", f"{onetime_count:,}",
                  delta=f"{onetime_count/total_cust*100:.1f}% of total")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### Count — Repeat vs One-Time")
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            repeat_df['Count'],
            labels=repeat_df['Type'],
            autopct='%1.1f%%',
            colors=['#2196F3', '#FF9800'],
            startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 3},
            textprops={'fontsize': 13}
        )
        ax.set_title("Customer Count Distribution", fontsize=13, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_right:
        st.markdown("#### Revenue Distribution by Customer Type")
        # Compute revenue share
        total_rev = customer_revenue['revenue'].sum()
        top_customers = customer_revenue.head(int(len(customer_revenue) * 0.2))
        top_rev_pct = top_customers['revenue'].sum() / total_rev * 100

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.barh(['One-Time', 'Repeat'],
                 [onetime_count / total_cust * 100, repeat_count / total_cust * 100],
                 color=['#FF9800', '#2196F3'])
        ax2.set_xlabel("% of Customers")
        ax2.set_title("Customer Breakdown (%)", fontsize=13, fontweight='bold')
        ax2.spines[['top', 'right']].set_visible(False)
        ax2.grid(axis='x', alpha=0.3)
        for i, v in enumerate([onetime_count / total_cust * 100, repeat_count / total_cust * 100]):
            ax2.text(v + 0.3, i, f"{v:.1f}%", va='center', fontsize=12, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    st.markdown("---")
    st.markdown("### 📋 Customer Revenue Table (Top 50)")
    top50 = customer_revenue.head(50).copy()
    top50.index = range(1, len(top50) + 1)
    top50['revenue'] = top50['revenue'].map('BRL {:,.2f}'.format)
    top50.columns = ['Customer Unique ID', 'Total Revenue']
    st.dataframe(top50, use_container_width=True, height=350)

    st.info(f"💡 **Insight:** Top 20% of customers account for **{top_rev_pct:.1f}%** of total revenue. This is close to the Pareto principle (80/20 rule).")

# ─────────────────────────────────────────────
#  PAGE: CATEGORIES
# ─────────────────────────────────────────────
elif page == "💰 Categories":
    st.markdown("# 💰 Product Category Revenue")
    st.markdown("---")

    n_cats = st.slider("Show Top N Categories", min_value=5, max_value=min(20, len(category_rev)), value=10)
    top_n  = category_rev.head(n_cats)

    fig, ax = plt.subplots(figsize=(12, n_cats * 0.6 + 1))
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, n_cats))
    bars = ax.barh(top_n['category'][::-1], top_n['revenue'][::-1],
                   color=colors, edgecolor='white')

    ax.set_xlabel("Total Revenue (BRL)", fontsize=11)
    ax.set_title(f"Top {n_cats} Product Categories by Revenue", fontsize=14, fontweight='bold')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'BRL {x/1e6:.1f}M'))
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.grid(axis='x', alpha=0.3)

    for bar, (_, row) in zip(bars, top_n[::-1].iterrows()):
        ax.text(bar.get_width() * 0.02, bar.get_y() + bar.get_height() / 2,
                f" BRL {row['revenue']:,.0f}",
                va='center', color='white', fontsize=9, fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("### 📋 Category Revenue Table")
    cat_display = category_rev.head(n_cats).copy()
    cat_display.index = range(1, len(cat_display) + 1)
    cat_display['revenue'] = cat_display['revenue'].map('BRL {:,.2f}'.format)
    cat_display.columns = ['Category', 'Total Revenue']
    st.dataframe(cat_display, use_container_width=True)
