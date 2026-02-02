import streamlit as st
from dashboard.task1 import task1_grouped_bar_chart

st.set_page_config(
    page_title="Google Play Store Analytics",
    layout="wide"
)

st.title("Google Play Store Data Analytics Dashboard")
st.markdown("""Task 1: This dashboard visualizes Google Play Store analytics based on task1 requirements.""")
st.divider()
st.subheader("Task 1: Average Rating vs Total Reviews")
visible_mode = False   # set True always the dashboard will visible
fig = task1_grouped_bar_chart(visible_mode=visible_mode)
if fig is None and not visible_mode:
    st.warning("This chart is available only between 3 PM and 5 PM IST.")
from dashboard.task2 import task2_dual_axis_chart
st.divider()
st.subheader("Task 2: Free vs Paid Apps – Installs & Revenue")
visible_mode = True
fig2 = task2_dual_axis_chart(visible_mode=visible_mode)
if fig2 is None:
    st.warning("TASK: 2 - This chart is available only between 1 PM and 2 PM IST.")


