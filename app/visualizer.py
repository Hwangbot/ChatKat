import plotly.express as px

def plot_revenue_trend(df):
    fig = px.line(df, x="year_month", y="revenue", title="Revenue Over Time")
    return fig

def plot_churn_trend(df):
    fig = px.line(df, x="year_month", y="churn_rate", title="Churn Rate Over Time")
    return fig

def plot_product_distribution(df):
    product_summary = df.groupby("product_id")["revenue"].sum().reset_index()
    fig = px.bar(product_summary, x="product_id", y="revenue", title="Revenue by Product")
    return fig