import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import streamlit as st


def is_time_allowed(start_hour, end_hour):
    ist = pytz.timezone("Asia/Kolkata")
    current_hour = datetime.now(ist).hour
    return start_hour <= current_hour < end_hour

def task2_dual_axis_chart(visible_mode=False):
    if not visible_mode and not is_time_allowed(13, 14):
        return None
    df = pd.read_csv("data/cleaned_apps.csv")
    df["Revenue"] = df["Price"] * df["Installs"]
    df["App_Name_Length"] = df["App"].str.len()
    filtered_df = df[
        (df["Installs"] >= 10000) &
        (df["Revenue"] >= 10000) &
        (df["Android Ver"].astype(str).str.extract(r"(\d+\.\d+)")[0].astype(float) > 4.0) &
        (df["Size_MB"] > 15) &
        (df["Content Rating"] == "Everyone") &
        (df["App_Name_Length"] <= 30)
    ]
    if filtered_df.empty:
        st.info("No data available after applying Task 2 filters.")
        return None
    top_categories = (
        filtered_df.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .index
    )

    filtered_df = filtered_df[filtered_df["Category"].isin(top_categories)]
    filtered_df["App_Type"] = filtered_df["Type"]
    summary_df = filtered_df.groupby("App_Type").agg(
        Avg_Installs=("Installs", "mean"),
        Avg_Revenue=("Revenue", "mean")
    )
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(
        summary_df.index,
        summary_df["Avg_Installs"],
        color="tab:blue",
        width=0.4,
        label="Average Installs"
    )
    ax1.set_ylabel("Average Installs")
    ax2 = ax1.twinx()
    ax2.bar(
        summary_df.index,
        summary_df["Avg_Revenue"],
        color="tab:orange",
        width=0.4,
        alpha=0.7,
        label="Average Revenue"
    )
    ax2.set_ylabel("Average Revenue ($)")
    ax1.set_title(
        "Average Installs vs Revenue\nFree vs Paid Apps (Top 3 Categories)"
    )
    ax1.set_xlabel("App Type")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.tight_layout()
    st.pyplot(fig)
    return fig
