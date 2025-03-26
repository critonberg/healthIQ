import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("🏋️‍♂️ Fitness Metrics Dashboard")

# Sidebar for data input
st.sidebar.header("Enter Your Health Data")
heart_rate = st.sidebar.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=75)
blood_pressure = st.sidebar.text_input("Blood Pressure (Systolic/Diastolic)", "120/80")
weight = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
sleep = st.sidebar.number_input("Sleep Hours", min_value=0.0, max_value=12.0, value=7.0)
steps = st.sidebar.number_input("Steps Taken", min_value=0, max_value=50000, value=10000)

# DataFrame to hold metrics
data = {
    "Metric": ["Heart Rate", "Blood Pressure", "Weight", "Sleep", "Steps"],
    "Value": [heart_rate, blood_pressure, weight, sleep, steps]
}
df = pd.DataFrame(data)

# Display key metrics
st.subheader("📊 Key Health Metrics")
st.dataframe(df, use_container_width=True)

# Visualization
st.subheader("📈 Trends Over Time")
time_series = pd.DataFrame({
    "Date": pd.date_range(start="2025-03-01", periods=7, freq='D'),
    "Heart Rate": [75, 80, 78, 76, 82, 85, heart_rate],
    "Steps": [10000, 9500, 10200, 11000, 12000, 9800, steps]
})
fig = px.line(time_series, x="Date", y=["Heart Rate", "Steps"], title="Health Trends")
st.plotly_chart(fig)

# Health Alerts
st.subheader("⚠️ Health Alerts")
if heart_rate > 100:
    st.error("High heart rate detected! Consider resting.")
if weight > 100:
    st.warning("Weight is above recommended levels. Consider monitoring diet.")
if sleep < 6:
    st.warning("You are not getting enough sleep. Try improving sleep habits.")
