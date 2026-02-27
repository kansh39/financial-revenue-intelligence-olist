# 📊 Financial & Revenue Intelligence Analysis – Olist E-commerce

This project performs end-to-end financial analytics on real-world Brazilian e-commerce data, including revenue trend analysis, customer churn evaluation, profitability insights, and time-series forecasting. The solution is deployed as an interactive Streamlit dashboard for executive decision-making.

A financial analytics dashboard built on real Brazilian e-commerce data (100K+ orders).

🔗 **Live Demo:** [Click to view dashboard](https://financial-revenue-intelligence-olist-fgf7gnmscdytcha57hgkle.streamlit.app/)

---

## 📌 What This Project Does

- Analyzes monthly revenue trends from 2016–2018
- Segments customers into Repeat vs One-Time buyers
- Forecasts next 3 months using Moving Average
- Breaks down revenue by product category
- Displays executive KPIs on an interactive dashboard

---

## 🛠️ Tech Stack

- Python, Pandas, NumPy, Matplotlib
- Streamlit (dashboard)
- Google Colab (data processing)
- Dataset: [Olist Brazilian E-Commerce — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## 📁 Files in This Repo

| File | Description |
|------|-------------|
| `app.py` | Streamlit dashboard code |
| `requirements.txt` | Python dependencies |
| `monthly_revenue.csv` | Revenue aggregated by month |
| `customer_revenue.csv` | Revenue per unique customer |
| `customer_repeat.csv` | Repeat vs one-time customer counts |
| `category_revenue.csv` | Revenue by product category |
| `kpi_summary.csv` | Executive KPI metrics |

---

## 🚀 Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/olist-revenue-dashboard.git
cd olist-revenue-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 💡 Key Insights

- 📈 Revenue grew steadily through 2018 with a clear peak month
- 👥 ~97% of customers are one-time buyers — retention is a major opportunity
- 💰 Health & Beauty and Watches are top revenue categories
- 🔮 3-month forecast suggests continued stable revenue

---

## 👤 Author

**Anshu Kumar**  
[LinkedIn](https://www.linkedin.com/in/anshuk674/) | [GitHub](https://github.com/kansh39)

*Built as a portfolio project for Data Analyst / Data Science roles.*
```

---

## Two things to update before pasting:

1. After your app deploys on Streamlit, **copy the live URL** and replace this line:
```
🔗 **Live Demo:** [Click to view dashboard](https://financial-revenue-intelligence-olist-fgf7gnmscdytcha57hgkle.streamlit.app/)
