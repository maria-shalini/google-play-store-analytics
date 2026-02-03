import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import streamlit as st

def is_time_allowed(start_hour, end_hour):
    ist = pytz.timezone("Asia/Kolkata")
    current_hour = datetime.now(ist).hour
    return start_hour <= current_hour < end_hour

def task5_bubble_chart(visible_mode=False):
    if not visible_mode and not is_time_allowed(17, 19):
        return None
    df = pd.read_csv("data/cleaned_apps.csv")
    allowed_categories = [
        "GAME", "BEAUTY", "BUSINESS", "COMICS",
        "COMMUNICATION", "DATING", "ENTERTAINMENT",
        "SOCIAL", "EVENTS"
    ]
    df = df[
        (df["Rating"] > 3.5) &
        (df["Installs"] > 50000) &
        (df["Reviews"] > 500) &
        (df["Sentiment_Subjectivity"] > 0.5) &
        (~df["App"].str.contains("S", case=False)) &
        (df["Category"].isin(allowed_categories))
    ]
    if df.empty:
        st.info("No data available after applying Task 5 filters.")
        return None
    category_translation = {
        "BEAUTY": "सौंदर्य",          # Hindi
        "BUSINESS": "வணிகம்",         # Tamil
        "DATING": "Partnersuche"      # German
    }
    df["Category_Label"] = df["Category"].map(
        lambda x: category_translation.get(x, x)
    )
    color_map = {
        "GAME": "pink",
        "सौंदर्य": "green",
        "வணிகம்": "blue",
        "Partnersuche": "purple",
        "COMICS": "orange",
        "COMMUNICATION": "red",
        "ENTERTAINMENT": "brown",
        "SOCIAL": "teal",
        "EVENTS": "gray"
    }
    fig = px.scatter(
        df,
        x="Size_MB",
        y="Rating",
        size="Installs",
        color="Category_Label",
        color_discrete_map=color_map,
        title="App Size vs Rating (Bubble Size = Installs)",
        hover_name="App",
        size_max=60
    )
    fig.update_layout(
        xaxis_title="App Size (MB)",
        yaxis_title="Average Rating",
        legend_title="App Category",
        hovermode="closest"
    )
    st.plotly_chart(fig, width="stretch")
    return fig
