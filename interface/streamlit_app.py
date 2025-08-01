# --- interface/streamlit_app.py (Enhanced with MCP toggle) ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from app.data_handler import clean_data, summarize_metrics
from app.summarizer import (
    generate_prompt,
    get_insights_from_llm
)
from app.visualizer import plot_revenue_trend, plot_churn_trend, plot_product_distribution
from app.history import init_db, save_insight_to_db, load_all_insights

st.set_page_config(page_title="ChatKat – Product Insights Bot", layout="centered")
st.title("ChatKat \U0001F43E – Your Product Insight Bot")

init_db()

uploaded_file = st.file_uploader("Upload a CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = clean_data(df)

    # Optional filtering
    if "product_id" in df.columns:
        product_choice = st.selectbox("Filter by Product ID", df["product_id"].unique())
        df = df[df["product_id"] == product_choice]

    summary = summarize_metrics(df)
    st.subheader("\U0001F4FE Summary")
    st.text(summary)

    # Charts
    st.subheader(" Visualizations")
    st.plotly_chart(plot_revenue_trend(df))

    if df["product_id"].nunique() > 1:
        st.plotly_chart(plot_product_distribution(df))
    else:
        st.info("Only one product selected — skipping product distribution chart.")

    if "churn_rate" in df.columns:
        st.plotly_chart(plot_churn_trend(df))

    insight_mode = st.radio("Select Insight Mode", ["Single Prompt", "MCP Chain"])

    if st.button(" Generate Insights"):
        if insight_mode == "Single Prompt":
            prompt = generate_prompt(summary)
            insights = get_insights_from_llm(prompt)
        else:
            description = get_insights_from_llm(f"Describe the data below in 3 bullet points:\n{summary}")
            insights_text = get_insights_from_llm(f"Based on this description, what are the 3 key business insights?\n{description}")
            actions = get_insights_from_llm(f"Given the following insights, suggest 3 business actions:\n{insights_text}")
            insights = f"### Description\n{description}\n\n### Insights\n{insights_text}\n\n### Actions\n{actions}"

        st.subheader("\U0001F4A1 AI Insights")
        st.markdown(insights)

        save_insight_to_db(uploaded_file.name, summary, insights)

    # Ask Me Anything
    st.subheader(" Ask Me Anything About Your Data")
    user_question = st.text_input("Your question:", placeholder="Why did revenue drop in April?")
    if user_question:
        q_prompt = f"""
        Data Summary:
        {summary}

        User Question: {user_question}

        Answer in plain English using business context.
        """
        answer = get_insights_from_llm(q_prompt)
        st.markdown("**Response:**")
        st.markdown(answer)

    # Show history
    if st.button(" View Past Insights"):
        st.subheader(" Insight History")
        for row in load_all_insights():
            st.markdown(f"**File:** {row[1]} |  {row[4]}")
            st.markdown(f"**Insights:**\n{row[3]}")
            st.markdown("---")
