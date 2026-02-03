import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import streamlit as st

def is_time_allowed(start_hour, end_hour):
    ist = pytz.timezone("Asia/Kolkata")
    current_hour = datetime.now(ist).hour
    return start_hour <= current_hour < end_hour

def task4_stacked_area_chart(visible_mode=False):

    if not visible_mode and not is_time_allowed(16, 18):
        return None

    df = pd.read_csv("data/cleaned_apps.csv")

    df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")
    df = df.dropna(subset=["Last Updated"])
    df["Month"] = df["Last Updated"].dt.to_period("M").astype(str)

    df = df[
        (df["Rating"] >= 4.2) &
        (df["Reviews"] > 1000) &
        (df["Size_MB"].between(20, 80)) &
        (df["Category"].str.startswith(("T", "P")))
    ]

    df = df[~df["App"].str.contains(r"\d", regex=True)]

    if df.empty:
        st.info("No data available after applying Task 4 filters.")
        return None

    monthly_df = (
        df.groupby(["Month", "Category"])
        .agg(Installs=("Installs", "sum"))
        .reset_index()
        .sort_values("Month")
    )

    monthly_df["Cumulative_Installs"] = (
        monthly_df.groupby("Category")["Installs"].cumsum()
    )

    category_translation = {
        "TRAVEL_AND_LOCAL": "Voyage et Local",  # French
        "PRODUCTIVITY": "Productividad",  # Spanish
        "PHOTOGRAPHY": "写真"  # Japanese
    }

    monthly_df["Category_Label"] = monthly_df["Category"].map(
        lambda x: category_translation.get(x, x)
    )

    monthly_df["Category_Label"] = pd.Categorical(
        monthly_df["Category_Label"],
        categories=monthly_df["Category_Label"].unique(),
        ordered=True
    )

    monthly_df["MoM_Growth"] = (
        monthly_df
        .groupby("Category")["Installs"]
        .pct_change()
    )

    if "MoM_Growth" in monthly_df.columns:
        highlight_months = monthly_df.loc[
            monthly_df["MoM_Growth"].fillna(0) > 0.25, "Month"
        ].unique()
    else:
        highlight_months = []
    monthly_df = monthly_df.drop(columns=["Category"])

    fig = px.area(
        monthly_df,
        x="Month",
        y="Cumulative_Installs",
        color="Category_Label",
        title="Cumulative App Installs Over Time (Filtered Categories)"
    )

    for month in highlight_months:
        fig.add_vrect(
            x0=month,
            x1=month,
            fillcolor="rgba(255, 0, 0, 0.30)",
            layer="below",
            line_width=0
        )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Cumulative Installs",
        legend_title="App Category",
        hovermode="x unified"
    )

    st.plotly_chart(fig, width="stretch")
    return fig
