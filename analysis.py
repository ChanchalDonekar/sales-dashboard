# analysis.py
print("Hello, Sales Analysis!")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1️⃣ Load dataset
df = pd.read_csv("sales dataset.csv.csv")  # Ensure filename matches exactly

# 2️⃣ Quick check
print("\nFirst 5 rows of the dataset:")
print(df.head(), "\n")

# 3️⃣ Missing values
print("Missing values in each column:")
print(df.isnull().sum(), "\n")

# 4️⃣ Duplicates
duplicates = df.duplicated().sum()
print(f"Total duplicate rows: {duplicates}\n")

# 5️⃣ Summary of numerical columns
print("Summary of numerical columns:")
print(df.describe(), "\n")

# 6️⃣ Convert Order_Date to datetime
if 'Order_Date' in df.columns:
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    print("Date conversion done for 'Order_Date' column.\n")

# 7️⃣ Total Revenue & Profit
total_revenue = df['Revenue'].sum()
total_profit = df['Profit'].sum()
print(f"Total Revenue: {total_revenue}")
print(f"Total Profit: {total_profit}\n")

# 8️⃣ Revenue & Profit by Region
if 'Region' in df.columns:
    region_summary = df.groupby('Region')[['Revenue','Profit']].sum()
    print("Revenue and Profit by Region:")
    print(region_summary, "\n")

    # Chart + save
    plt.figure(figsize=(8,5))
    sns.barplot(x=region_summary.index, y='Revenue', data=region_summary.reset_index())
    plt.title("Revenue by Region")
    plt.ylabel("Revenue")
    plt.xlabel("Region")
    plt.savefig("Revenue_by_Region.png")
    plt.show()

# 9️⃣ Revenue & Profit by Payment Method
if 'Payment_Method' in df.columns:
    payment_summary = df.groupby('Payment_Method')[['Revenue','Profit']].sum()
    print("Revenue and Profit by Payment Method:")
    print(payment_summary, "\n")

    # Chart + save
    plt.figure(figsize=(8,5))
    sns.barplot(x=payment_summary.index, y='Revenue', data=payment_summary.reset_index())
    plt.title("Revenue by Payment Method")
    plt.xticks(rotation=45)
    plt.ylabel("Revenue")
    plt.xlabel("Payment Method")
    plt.savefig("Revenue_by_PaymentMethod.png")
    plt.show()

# 🔟 Top-selling products by Quantity
if 'Product_Category' in df.columns:
    top_products = df.groupby('Product_Category')['Quantity'].sum().sort_values(ascending=False)
    print("Top-selling products (by quantity sold):")
    print(top_products, "\n")
    
    top_product = top_products.idxmax()
    top_qty = top_products.max()
    print(f"Top product overall: {top_product} with {top_qty} units sold\n")

    # Chart + save
    plt.figure(figsize=(8,5))
    sns.barplot(x=top_products.index, y=top_products.values)
    plt.title("Top-selling Products (Quantity)")
    plt.ylabel("Quantity Sold")
    plt.xlabel("Product Category")
    plt.xticks(rotation=45)
    plt.savefig("TopProducts_Quantity.png")
    plt.show()

# 1️⃣1️⃣ Monthly Revenue & Profit
if 'Order_Date' in df.columns:
    df['Month'] = df['Order_Date'].dt.to_period('M')
    monthly_summary = df.groupby('Month')[['Revenue','Profit']].sum()
    print("Monthly Revenue & Profit trends:")
    print(monthly_summary, "\n")

    # Chart + save
    plt.figure(figsize=(10,5))
    monthly_summary['Revenue'].plot(label="Revenue")
    monthly_summary['Profit'].plot(label="Profit")
    plt.title("Monthly Revenue & Profit")
    plt.ylabel("Amount")
    plt.xlabel("Month")
    plt.legend()
    plt.xticks(rotation=45)
    plt.savefig("Monthly_Revenue_Profit.png")
    plt.show()

# 1️⃣2️⃣ Correlation Heatmap
numeric_cols = df.select_dtypes(include='number')
plt.figure(figsize=(10,7))
sns.heatmap(numeric_cols.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("Correlation_Heatmap.png")
plt.show()

print("All charts saved as PNG files in the current folder!")
# ===== EXTRA INSIGHTS & REPORT STYLE CHARTS =====

# 🔹 Top 3 Product Categories by Revenue
top3_products = df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False).head(3)
print("Top 3 products by Revenue:")
print(top3_products, "\n")

plt.figure(figsize=(8,5))
sns.barplot(x=top3_products.index, y=top3_products.values, palette="viridis")
plt.title("Top 3 Products by Revenue")
plt.ylabel("Revenue")
plt.xlabel("Product Category")
plt.savefig("Top3_Products_Revenue.png")
plt.show()

# 🔹 Revenue & Profit by Customer Segment
if 'Customer_Segment' in df.columns:
    segment_summary = df.groupby('Customer_Segment')[['Revenue','Profit']].sum()
    print("Revenue and Profit by Customer Segment:")
    print(segment_summary, "\n")

    plt.figure(figsize=(8,5))
    sns.barplot(x=segment_summary.index, y='Revenue', data=segment_summary.reset_index(), palette="magma")
    plt.title("Revenue by Customer Segment")
    plt.ylabel("Revenue")
    plt.xlabel("Customer Segment")
    plt.xticks(rotation=30)
    plt.savefig("Revenue_by_CustomerSegment.png")
    plt.show()

# 🔹 Highest Revenue & Profit Region
if 'Region' in df.columns:
    highest_revenue_region = region_summary['Revenue'].idxmax()
    highest_profit_region = region_summary['Profit'].idxmax()
    print("===== TOP INSIGHTS =====")
    print(f"Highest Revenue Region: {highest_revenue_region} ({region_summary['Revenue'].max()})")
    print(f"Highest Profit Region: {highest_profit_region} ({region_summary['Profit'].max()})")
    
# 🔹 Month with Highest Revenue
max_revenue_month = monthly_summary['Revenue'].idxmax()
print(f"Month with Highest Revenue: {max_revenue_month} ({monthly_summary['Revenue'].max()})")
print("========================\n")