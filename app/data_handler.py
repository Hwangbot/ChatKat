import pandas as pd
import numpy as np

def clean_data(df):
    # Ensure all column names are strings
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    
    # Drop rows where all values are NaN
    df = df.dropna(how="all")

    return df

def summarize_metrics(df):
    summary = []

    if "revenue" in df.columns:
        avg_revenue = df["revenue"].mean()
        std_revenue = df["revenue"].std()
        summary.append(f"Average revenue: {avg_revenue:.2f}")
        summary.append(f"Revenue standard deviation: {std_revenue:.2f}")

    if "churn_rate" in df.columns:
        avg_churn = df["churn_rate"].mean()
        summary.append(f"Average churn rate: {avg_churn:.2%}")

    return "\n".join(summary)
