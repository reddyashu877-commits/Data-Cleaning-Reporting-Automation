import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output folders
os.makedirs("output", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Load data
df = pd.read_csv("data/sales_data.csv")

print("Original Data:")
print(df)

# -----------------------------
# DATA CLEANING
# -----------------------------

# Remove duplicate rows
df = df.drop_duplicates()

# Convert date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert numeric columns
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Fill missing Quantity with median
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())

# Fill missing Price with median
df["Price"] = df["Price"].fillna(df["Price"].median())

# Standardize text
df["Category"] = df["Category"].str.title()
df["Region"] = df["Region"].str.title()
df["Product"] = df["Product"].str.title()
df["Salesperson"] = df["Salesperson"].str.title()

# Calculate total sales
df["Total_Sales"] = df["Quantity"] * df["Price"]

# Save cleaned data
cleaned_file = "output/cleaned_sales_data.csv"
df.to_csv(cleaned_file, index=False)

print("\nCleaned Data:")
print(df)

# -----------------------------
# REPORT GENERATION
# -----------------------------

total_sales = df["Total_Sales"].sum()
total_quantity = df["Quantity"].sum()
average_sales = df["Total_Sales"].mean()

print("\nREPORT")
print("-------------------------")
print("Total Sales:", total_sales)
print("Total Quantity:", total_quantity)
print("Average Sales:", average_sales)

# -----------------------------
# CHART 1 - SALES BY PRODUCT
# -----------------------------

product_sales = df.groupby("Product")["Total_Sales"].sum()

plt.figure(figsize=(8, 5))
product_sales.plot(kind="bar")
plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("charts/sales_by_product.png")
plt.close()

# -----------------------------
# CHART 2 - SALES BY REGION
# -----------------------------

region_sales = df.groupby("Region")["Total_Sales"].sum()

plt.figure(figsize=(8, 5))
region_sales.plot(kind="bar")
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("charts/sales_by_region.png")
plt.close()

# -----------------------------
# EXCEL REPORT
# -----------------------------

with pd.ExcelWriter("output/automated_sales_report.xlsx", engine="openpyxl") as writer:

    df.to_excel(writer, sheet_name="Cleaned Data", index=False)

    summary = pd.DataFrame({
        "Metric": [
            "Total Sales",
            "Total Quantity",
            "Average Sales"
        ],
        "Value": [
            total_sales,
            total_quantity,
            average_sales
        ]
    })

    summary.to_excel(writer, sheet_name="Summary", index=False)

print("\nProject completed successfully!")
print("Cleaned data saved to:", cleaned_file)
print("Excel report saved to: output/automated_sales_report.xlsx")
print("Charts saved in the charts folder.")
