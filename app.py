import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Analysis Dashboard (Pro Version)")

# =========================
# Load Data
# =========================
df = pd.read_csv("sales dataset.csv.csv")

if 'Order_Date' in df.columns:
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# =========================
# Sidebar Filters
# =========================
st.sidebar.header("🔎 Filters")

# Region Filter
if 'Region' in df.columns:
    selected_region = st.sidebar.multiselect(
        "Select Region",
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )
    df = df[df['Region'].isin(selected_region)]

# Payment Method Filter
if 'Payment_Method' in df.columns:
    selected_payment = st.sidebar.multiselect(
        "Select Payment Method",
        options=df['Payment_Method'].unique(),
        default=df['Payment_Method'].unique()
    )
    df = df[df['Payment_Method'].isin(selected_payment)]

# Date Range Filter
if 'Order_Date' in df.columns:
    min_date = df['Order_Date'].min()
    max_date = df['Order_Date'].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date]
    )

    if len(date_range) == 2:
        df = df[(df['Order_Date'] >= pd.to_datetime(date_range[0])) &
                (df['Order_Date'] <= pd.to_datetime(date_range[1]))]

# =========================
# KPI Section
# =========================
total_revenue = df['Revenue'].sum()
total_profit = df['Profit'].sum()
total_orders = len(df)
total_quantity = df['Quantity'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"{total_revenue:,.0f}")
col2.metric("📈 Total Profit", f"{total_profit:,.0f}")
col3.metric("🛒 Total Orders", total_orders)
col4.metric("📦 Total Quantity Sold", total_quantity)

st.markdown("---")

# =========================
# Charts Section
# =========================

colA, colB = st.columns(2)

# Revenue by Region
if 'Region' in df.columns:
    with colA:
        st.subheader("Revenue by Region")
        region_summary = df.groupby('Region')['Revenue'].sum().reset_index()
        fig1, ax1 = plt.subplots()
        sns.barplot(data=region_summary, x='Region', y='Revenue', ax=ax1)
        plt.xticks(rotation=45)
        st.pyplot(fig1)

# Revenue by Payment Method
if 'Payment_Method' in df.columns:
    with colB:
        st.subheader("Revenue by Payment Method")
        payment_summary = df.groupby('Payment_Method')['Revenue'].sum().reset_index()
        fig2, ax2 = plt.subplots()
        sns.barplot(data=payment_summary, x='Payment_Method', y='Revenue', ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

# Monthly Trend
if 'Order_Date' in df.columns:
    st.subheader("📅 Monthly Revenue & Profit Trend")
    df['Month'] = df['Order_Date'].dt.to_period('M')
    monthly = df.groupby('Month')[['Revenue', 'Profit']].sum()

    fig3, ax3 = plt.subplots(figsize=(10,5))
    monthly['Revenue'].plot(label="Revenue", ax=ax3)
    monthly['Profit'].plot(label="Profit", ax=ax3)
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig3)

# Top Products
if 'Product_Category' in df.columns:
    st.subheader("🏆 Top Selling Products (Quantity)")
    top_products = df.groupby('Product_Category')['Quantity'].sum().sort_values(ascending=False)

    fig4, ax4 = plt.subplots()
    sns.barplot(x=top_products.index, y=top_products.values, ax=ax4)
    plt.xticks(rotation=45)
    st.pyplot(fig4)

st.success("✅ Professional Dashboard Loaded Successfully!")