import pandas as pd
import numpy as np

# Load your datasets
purchase_df = pd.read_csv("sample_data/purchase_history_dataset.csv")

# Convert date column
purchase_df["purchase_date"] = pd.to_datetime(purchase_df["purchase_date"], errors="coerce")

# Create a year-month column
purchase_df["year_month"] = purchase_df["purchase_date"].dt.to_period("M").astype(str)

# Group by product and month
usage_df = (
    purchase_df
    .groupby(["product_id", "year_month"])
    .agg(
        units_sold=("quantity", "sum"),
        revenue=("total_amount", "sum"),
        customer_count=("customer_id", pd.Series.nunique)
    )
    .reset_index()
)

# Simulate churn rate
np.random.seed(42)
usage_df["churn_rate"] = np.round(np.random.uniform(0.01, 0.30, size=len(usage_df)), 3)

# Save the result
usage_df.to_csv("sample_data/product_usage.csv", index=False)
print(" product_usage.csv created successfully!")
