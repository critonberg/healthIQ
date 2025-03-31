import streamlit as st
import pandas as pd
import plotly.express as px
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
        'Sleep (Hours)': (6 + (pd.Series(range(30)) % 3)).tolist()
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
st.metric(label="Average Blood Pressure", value=f"{int(df['Blood Pressure (Systolic)'].mean())}/{int(df['Blood Pressure (Diastolic)'].mean())} mmHg")
st.metric(label="Average Sleep Duration", value=f"{df['Sleep (Hours)'].mean():.1f} hours")

# Charts
st.subheader("Progress Charts")
fig_steps = px.line(df, x='Date', y='Steps', title='Daily Steps', markers=True)
fig_heart = px.line(df, x='Date', y='Heart Rate', title='Heart Rate Over Time', markers=True)
fig_weight = px.line(df, x='Date', y='Weight', title='Weight Trend', markers=True)

# Blood Pressure Area Chart
fig_bp = px.area(df, x='Date', y=['Blood Pressure (Systolic)', 'Blood Pressure (Diastolic)'],
                 title='Blood Pressure Trends', labels={'value': 'Blood Pressure (mmHg)', 'variable': 'Type'},
                 markers=True)

# Sleep Pattern Violin Plot
fig_sleep = px.violin(df, y='Sleep (Hours)', box=True, points='all',
                      title='Sleep Pattern Distribution',
                      labels={'Sleep (Hours)': 'Hours of Sleep'})

st.plotly_chart(fig_steps)
st.plotly_chart(fig_heart)
st.plotly_chart(fig_weight)
st.plotly_chart(fig_bp)
st.plotly_chart(fig_sleep)

# Data Table
st.subheader("Detailed Breakdown")
st.dataframe(df)

# Export to Excel Function
def export_excel(data):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        data.to_excel(writer, sheet_name='Report', index=False)
    return buffer.getvalue()

# Excel Download Button
st.download_button(
    label="Download Report as Excel",
    data=export_excel(df),
    file_name="fitness_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
