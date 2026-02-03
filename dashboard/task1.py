import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import streamlit as st


def is_time_allowed(start_hour, end_hour):
    ist = pytz.timezone("Asia/Kolkata")
    current_hour = datetime.now(ist).hour
    return start_hour <= current_hour < end_hour


def task1_grouped_bar_chart(visible_mode=False):
    if not visible_mode and not is_time_allowed(15, 17):
        return None
    df = pd.read_csv("data/cleaned_apps.csv")
    df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")
    st.sidebar.header("Task 1 Filters")
    min_rating = st.sidebar.slider(
        "Minimum Average Rating",
        min_value=4.0,
        max_value=5.0,
        value=4.0,
        step=0.1
    )
    max_size = st.sidebar.slider(
        "Maximum App Size (MB)",
        min_value=1,
        max_value=50,
        value=10
    )
    filtered_df = df[
        (df["Rating"] >= min_rating) &
        (df["Size_MB"] <= max_size) &
        (df["Last Updated"].dt.month == 1)
        ]
    if filtered_df.empty:
        st.info("No data available for selected filters.")
        return None
    top_categories = (
        filtered_df.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )
    selected_categories = st.sidebar.multiselect(
        "Select App Categories",
        options=top_categories,
        default=list(top_categories)
    )
    final_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
    if final_df.empty:
        st.warning("Please select at least one category.")
        return None
    summary_df = final_df.groupby("Category").agg(
        Average_Rating=("Rating", "mean"),
        Total_Reviews=("Reviews", "sum")
    )
    fig, ax1 = plt.subplots(figsize=(12, 6))
    x = range(len(summary_df.index))
    ax1.bar(
        x,
        summary_df["Average_Rating"],
        color="tab:blue",
        width=0.4,
        label="Average Rating"
    )
    ax1.set_ylabel("Average Rating")
    ax1.set_ylim(0, 5)
    ax2 = ax1.twinx()
    ax2.bar(
        x,
        summary_df["Total_Reviews"],
        color="tab:orange",
        width=0.4,
        alpha=0.7,
        label="Total Reviews"
    )
    ax2.set_ylabel("Total Reviews")
    ax1.set_title(
        "Average Rating vs Total Reviews\nTop 10 App Categories by Installs"
    )
    ax1.set_xlabel("App Category")
    ax1.set_xticks(x)
    ax1.set_xticklabels(summary_df.index, rotation=45, ha="right")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.tight_layout()
    st.pyplot(fig)
    return fig
