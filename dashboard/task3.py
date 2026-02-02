import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import streamlit as st

def is_time_allowed(start_hour, end_hour):
    ist = pytz.timezone("Asia/Kolkata")
    current_hour = datetime.now(ist).hour
    return start_hour <= current_hour < end_hour

def task3_choropleth_map(visible_mode=False):
    if not visible_mode and not is_time_allowed(18, 20):
        return None
    df = pd.read_csv("data/cleaned_apps.csv")
    df = df.dropna(subset=["Category", "Installs", "Country"])
    df = df[~df["Category"].str.startswith(("A", "C", "G", "S"))]
    if df.empty:
        st.info("No data available after category exclusion.")
        return None
    top_categories = (
        df.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .index
    )
    df = df[df["Category"].isin(top_categories)]
    summary_df = (
        df.groupby(["Country", "Category"])
        .agg(Total_Installs=("Installs", "sum"))
        .reset_index()
    )
    st.sidebar.header("Task 3 Filters")
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=top_categories,
        default=list(top_categories)
    )
    summary_df = summary_df[summary_df["Category"].isin(selected_categories)]
    if summary_df.empty:
        st.warning("No data available for selected categories.")
        return None
    summary_df["Highlight"] = summary_df["Total_Installs"].apply(
        lambda x: "Above 1M" if x > 1_000_000 else "Below 1M"
    )
    fig = px.choropleth(
        summary_df,
        locations="Country",
        locationmode="country names",
        color="Total_Installs",
        hover_name="Category",
        hover_data={
            "Total_Installs": ":,",
            "Country": True,
            "Highlight": True
        },
        color_continuous_scale="Viridis",
        title="Global App Installs by Category (Top 5)"
    )
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    return fig
