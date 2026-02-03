import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import streamlit as st

def is_time_allowed(start_hour, end_hour):
    ist = pytz.timezone("Asia/Kolkata")
    current_hour = datetime.now(ist).hour
    return start_hour <= current_hour < end_hour

def task6_time_series_chart(visible_mode=False):
    if not visible_mode and not is_time_allowed(18, 21):
        return None
    df = pd.read_csv("data/cleaned_apps.csv")
    df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")
    df = df.dropna(subset=["Last Updated"])
    df["Month"] = df["Last Updated"].dt.to_period("M").astype(str)
    df = df[
        (df["Reviews"] > 500) &
        (~df["App"].str.lower().str.startswith(("x", "y", "z"))) &
        (~df["App"].str.contains("S", case=False)) &
        (df["Category"].str.startswith(("E", "C", "B")))
    ]
    if df.empty:
        st.info("No data available after applying Task 6 filters.")
        return None
    monthly_df = (
        df.groupby(["Month", "Category"])
        .agg(Total_Installs=("Installs", "sum"))
        .reset_index()
        .sort_values("Month")
    )
    category_translation = {
        "BEAUTY": "सौंदर्य",
        "BUSINESS": "வணிகம்",
        "DATING": "Partnersuche"
    }
    monthly_df["Category_Label"] = monthly_df["Category"].apply(
        lambda x: category_translation.get(x, x)
    )
    monthly_df["Category_Label"] = pd.Categorical(
        monthly_df["Category_Label"],
        categories=(
            monthly_df.groupby("Category_Label")["Total_Installs"]
            .sum()
            .sort_values(ascending=False)
            .index
        ),
        ordered=True
    )
    monthly_df["MoM_Growth"] = (
        monthly_df
        .groupby("Category")["Total_Installs"]
        .pct_change()
    )
    highlight_months = monthly_df.loc[
        monthly_df["MoM_Growth"].fillna(0) > 0.20, "Month"
    ].unique()
    fig = px.line(
        monthly_df,
        x="Month",
        y="Total_Installs",
        color="Category_Label",
        title="Total Installs Trend Over Time by App Category"
    )
    for month in highlight_months:
        fig.add_vrect(
            x0=month,
            x1=month,
            fillcolor="rgba(0, 255, 0, 0.25)",
            layer="below",
            line_width=0
        )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Installs",
        legend_title="App Category",
        hovermode="x unified"
    )
    st.plotly_chart(fig, width="stretch")
    return fig
