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
    st.warning("Task 1: This chart is available only between 3 PM and 5 PM IST.")
from dashboard.task2 import task2_dual_axis_chart
st.divider()
st.subheader("Task 2: Free vs Paid Apps – Installs & Revenue")
visible_mode = False   # set True always the dashboard will visible
fig2 = task2_dual_axis_chart(visible_mode=visible_mode)
if fig2 is None:
    st.warning("Task: 2 - This chart is available only between 1 PM and 2 PM IST.")
from dashboard.task3 import task3_choropleth_map
st.divider()
st.subheader("Task 3: Global Installs by Category (Choropleth Map)")
visible_mode = False   # set True always the dashboard will visible
fig3 = task3_choropleth_map(visible_mode=visible_mode)
if fig3 is None:
    st.warning("Task 3: This map is available only between 6 PM and 8 PM IST.")
