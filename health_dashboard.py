import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO

# Sample Data Generation Function
def generate_sample_data():
    dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
    data = {
        'Date': dates,
        'Steps': (8000 + (1000 * (pd.Series(range(30)) % 5))).tolist(),
        'Heart Rate': (70 + (5 * (pd.Series(range(30)) % 4))).tolist(),
        'Weight': (75 - (0.2 * pd.Series(range(30)))).tolist(),
        'Blood Pressure (Systolic)': (120 + (pd.Series(range(30)) % 5)).tolist(),
        'Blood Pressure (Diastolic)': (80 + (pd.Series(range(30)) % 3)).tolist(),
        'Sleep (Hours)': np.random.uniform(5, 9, 30).tolist()  # More realistic sleep data
    }
    return pd.DataFrame(data)

# Generate Data
df = generate_sample_data()

# Streamlit UI
st.title("Monthly Fitness Report")

# Summary Metrics
st.subheader("Summary")
st.metric(label="Average Steps", value=int(df['Steps'].mean()))
st.metric(label="Average Heart Rate", value=int(df['Heart Rate'].mean()))
st.metric(label="Weight Change", value=f"{df['Weight'].iloc[-1] - df['Weight'].iloc[0]:.1f} kg")
st.metric(label="Average Blood Pressure",
          value=f"{int(df['Blood Pressure (Systolic)'].mean())}/{int(df['Blood Pressure (Diastolic)'].mean())} mmHg")
st.metric(label="Average Sleep Duration", value=f"{df['Sleep (Hours)'].mean():.1f} hours")

# Charts
st.subheader("Progress Charts")
fig_steps = px.line(df, x='Date', y='Steps', title='Daily Steps', markers=True)
fig_heart = px.line(df, x='Date', y='Heart Rate', title='Heart Rate Over Time', markers=True)
fig_weight = px.line(df, x='Date', y='Weight', title='Weight Trend', markers=True)

# Blood Pressure Area Chart
fig_bp = px.area(df, x='Date', y=['Blood Pressure (Systolic)', 'Blood Pressure (Diastolic)'],
                 title='Blood Pressure Trends', labels={'value': 'Blood Pressure (mmHg)', 'variable': 'Type'})

# Sleep Pattern Line Chart
fig_sleep_line = px.line(df, x='Date', y='Sleep (Hours)', title='Sleep Duration Over Time', markers=True)

# Display Charts
st.plotly_chart(fig_steps)
st.plotly_chart(fig_heart)
st.plotly_chart(fig_weight)
st.plotly_chart(fig_bp)
st.plotly_chart(fig_sleep_line)

# Data Table
st.subheader("Detailed Breakdown")
st.dataframe(df)

# Export to Excel Function (Using openpyxl instead of xlsxwriter)
def export_excel(data):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:  # Use openpyxl instead
        data.to_excel(writer, sheet_name='Report', index=False)
    buffer.seek(0)  # Move pointer to the beginning
    return buffer.getvalue()

# Excel Download Button
st.download_button(
    label="Download Report as Excel",
    data=export_excel(df),
    file_name="fitness_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Goal Setting Section
st.sidebar.header("Set Your Health Goals")
steps_goal = st.sidebar.number_input("Daily Steps Goal", min_value=1000, value=10000, step=500)
weight_goal = st.sidebar.number_input("Target Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
sleep_goal = st.sidebar.number_input("Daily Sleep Goal (hours)", min_value=4.0, max_value=12.0, value=8.0, step=0.5)

st.sidebar.write(f"**Your Goals:**\n - Steps: {steps_goal}\n - Weight: {weight_goal} kg\n - Sleep: {sleep_goal} hours")
