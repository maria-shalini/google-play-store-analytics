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

    df["Android_Version"] = (
        df["Android Ver"]
        .astype(str)
        .str.extract(r"(\d+\.\d+)")[0]
    )
    df["Android_Version"] = pd.to_numeric(df["Android_Version"], errors="coerce")
    base_df = df[
        (df["Installs"] >= 10000) &
        (df["Android_Version"] > 4.0) &
        (df["Size_MB"] > 15) &
        (df["Content Rating"] == "Everyone") &
        (df["App_Name_Length"] <= 30)
    ]
    if base_df.empty:
        st.info("No data available after applying Task 2 filters.")
        return None
    paid_df = base_df[
        (base_df["Type"] == "Paid") &
        (base_df["Revenue"] >= 10000)
    ]
    free_df = base_df[base_df["Type"] == "Free"]
    filtered_df = pd.concat([free_df, paid_df])
    top_categories = (
        filtered_df.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .index
    )
    filtered_df = filtered_df[filtered_df["Category"].isin(top_categories)]
    st.sidebar.header("Task 2 Filters")

    app_type_filter = st.sidebar.radio(
        "Select App Type",
        options=["Both", "Free", "Paid"],
        index=0
    )
    category_filter = st.sidebar.multiselect(
        "Top 3 Categories",
        options=list(top_categories),
        default=list(top_categories)
    )
    show_revenue = st.sidebar.checkbox(
        "Show Revenue Axis",
        value=True
    )
    if app_type_filter != "Both":
        filtered_df = filtered_df[filtered_df["Type"] == app_type_filter]
    filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]
    if filtered_df.empty:
        st.warning("No data for selected filters.")
        return None
    summary_df = filtered_df.groupby("Type").agg(
        Avg_Installs=("Installs", "mean"),
        Avg_Revenue=("Revenue", "mean")
    )
    summary_df = summary_df.reindex(["Free", "Paid"]).dropna(how="all")
    fig, ax1 = plt.subplots(figsize=(10, 6))
    x = range(len(summary_df.index))
    width = 0.35
    ax1.bar(
        [i - width / 2 for i in x],
        summary_df["Avg_Installs"],
        width=width,
        label="Average Installs",
        color="tab:blue"
    )
    ax1.set_ylabel("Average Installs")
    if show_revenue:
        ax2 = ax1.twinx()
        ax2.bar(
            [i + width / 2 for i in x],
            summary_df["Avg_Revenue"],
            width=width,
            label="Average Revenue",
            color="tab:orange"
        )
        ax2.set_ylabel("Average Revenue ($)")
        ax2.legend(loc="upper right")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(summary_df.index)
    ax1.set_xlabel("App Type")
    ax1.set_title("Average Installs vs Revenue\nFree vs Paid Apps (Top 3 Categories)")
    ax1.legend(loc="upper left")
    plt.tight_layout()
    st.pyplot(fig)
    return fig
