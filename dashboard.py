import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ✅ Set page configuration at the very top
st.set_page_config(page_title="HealthIQ Dashboard", layout="wide")

# Create tabs
tab1, tab2 = st.tabs(["📊 Fitness Dashboard", "🥗 Nutrition Advice"])

# 🏋️‍♂️ FITNESS DASHBOARD
with tab1:
    st.title("🏋️‍♂️ Fitness Metrics Dashboard")
    st.markdown("Monitor your key health metrics and track progress over time.")

    # Sidebar for data input
    st.sidebar.header("🔢 Enter Your Health Data")
    heart_rate = st.sidebar.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=75)
    systolic_bp = st.sidebar.number_input("Systolic Blood Pressure", min_value=50, max_value=200, value=120)
    diastolic_bp = st.sidebar.number_input("Diastolic Blood Pressure", min_value=30, max_value=130, value=80)
    weight = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
    sleep = st.sidebar.number_input("Sleep Hours", min_value=0.0, max_value=12.0, value=7.0)
    steps = st.sidebar.number_input("Steps Taken", min_value=0, max_value=50000, value=10000)

    # Generate realistic health variations
    dates = pd.date_range(start="2025-03-01", periods=7, freq='D')
    heart_rate_variation = np.random.randint(65, 95, size=len(dates) - 1).tolist() + [heart_rate]
    steps_variation = np.random.randint(8000, 15000, size=len(dates) - 1).tolist() + [steps]

    # DataFrame to hold metrics
    df = pd.DataFrame({
        "Metric": ["Heart Rate (bpm)", "Blood Pressure (mmHg)", "Weight (kg)", "Sleep (hours)", "Steps Taken"],
        "Value": [heart_rate, f"{systolic_bp}/{diastolic_bp}", weight, sleep, steps]
    })

    # Display key metrics with formatting
    st.subheader("📊 Key Health Metrics")
    st.dataframe(df, use_container_width=True)

    # 📈 Trends Over Time - Heart Rate & Steps
    st.subheader("📈 Trends Over Time")
    time_series = pd.DataFrame({
        "Date": dates,
        ##"Heart Rate": heart_rate_variation,
        "Steps": steps_variation
    })
    fig_heart_steps = px.line(time_series, x="Date", y=["Steps"],
                              title="Steps Trends", markers=True)
    st.plotly_chart(fig_heart_steps, use_container_width=True)

    # 🎯 Gauge Chart for Weight
    fig_weight = go.Figure(go.Indicator(
        mode="gauge+number",
        value=weight,
        title={"text": "Weight (kg)"},
        gauge={
            "axis": {"range": [30, 200]},
            "steps": [
                {"range": [30, 60], "color": "lightgray"},
                {"range": [60, 100], "color": "lightblue"},
                {"range": [100, 150], "color": "yellow"},
                {"range": [150, 200], "color": "red"}
            ]
        }
    ))
    st.plotly_chart(fig_weight, use_container_width=True)

    # 📊 Bar Chart for Blood Pressure
    fig_bp = go.Figure()
    fig_bp.add_trace(go.Bar(
        x=["Systolic", "Diastolic"],
        y=[systolic_bp, diastolic_bp],
        ##text=[systolic_bp, diastolic_bp],
        textposition='auto',
        marker_color=['blue', 'red']
    ))
    fig_bp.update_layout(title="Blood Pressure Levels", xaxis_title="Type", yaxis_title="mmHg")
    st.plotly_chart(fig_bp, use_container_width=True)

    # ⚠️ Health Alerts
    st.subheader("⚠️ Health Alerts")
    alert_messages = []
    if heart_rate > 100:
        alert_messages.append("🚨 High heart rate detected! Consider resting.")
    if systolic_bp > 130 or diastolic_bp > 90:
        alert_messages.append("⚠️ High blood pressure detected! Consider consulting a doctor.")
    if weight > 100:
        alert_messages.append("⚠️ Weight is above recommended levels. Consider monitoring diet.")
    if sleep < 6:
        alert_messages.append("⚠️ You are not getting enough sleep. Try improving sleep habits.")
    if steps < 5000:
        alert_messages.append("⚠️ Low activity detected. Try to walk more for better health.")

    if alert_messages:
        for alert in alert_messages:
            st.error(alert)
    else:
        st.success("✅ All health metrics are within a good range!")

# 🥗 NUTRITION ADVICE
with tab2:
    st.title("🥗 Personalized Nutrition Advice")
    st.markdown("Get tailored nutrition suggestions based on your health metrics.")

    # Long-form nutrition suggestions
    nutrition_advice = []

    ## ⚖️ Weight Management
    if weight > 100:
        nutrition_advice.append("🍏 **Increase Fiber Intake**: High-fiber foods like vegetables, beans, and whole grains help keep you full for longer, reducing unnecessary snacking and aiding in weight loss.")
        nutrition_advice.append("🛑 **Reduce Sugar & Processed Foods**: Processed foods contain unhealthy fats and sugars that contribute to weight gain. Replace sugary drinks with water or herbal tea.")
        nutrition_advice.append("🍗 **Prioritize Lean Proteins**: Proteins like chicken, turkey, fish, and tofu promote muscle growth and increase metabolism, aiding weight management.")
        nutrition_advice.append("🥜 **Eat Healthy Fats**: Avocados, nuts, and olive oil provide essential fatty acids that support brain function while keeping hunger in check.")

    ## ❤️ Heart Health (High Heart Rate)
    if heart_rate > 100:
        nutrition_advice.append("🥑 **Eat Magnesium-Rich Foods**: Nuts, seeds, and leafy greens help regulate heart rate and reduce stress on the cardiovascular system.")
        nutrition_advice.append("☕ **Limit Caffeine & Alcohol**: Stimulants can elevate heart rate. Swap coffee with green tea, which contains antioxidants that support heart health.")
        nutrition_advice.append("🍓 **Consume Omega-3 Fatty Acids**: Fatty fish (salmon, mackerel) and flaxseeds help maintain normal heart function and reduce inflammation.")

    ## 🩸 Blood Pressure (Hypertension)
    if systolic_bp > 130 or diastolic_bp > 90:
        nutrition_advice.append("🍌 **Increase Potassium Intake**: Bananas, oranges, potatoes, and spinach help balance sodium levels, reducing blood pressure.")
        nutrition_advice.append("🧂 **Reduce Sodium (Salt) Consumption**: Too much salt can raise blood pressure. Choose fresh foods and avoid processed meals high in sodium.")
        nutrition_advice.append("🥑 **Eat More Healthy Fats**: Olive oil, nuts, and seeds contain monounsaturated fats that support healthy blood pressure levels.")
        nutrition_advice.append("🥕 **Incorporate More Antioxidants**: Berries, carrots, and dark chocolate help relax blood vessels and improve circulation.")

    ## 💤 Sleep Improvement
    if sleep < 6:
        nutrition_advice.append("🥛 **Consume Magnesium & Melatonin-Rich Foods**: Almonds, walnuts, and cherries promote better sleep quality.")
        nutrition_advice.append("🍵 **Drink Herbal Teas**: Chamomile tea and valerian root tea help calm the nervous system, making it easier to fall asleep.")
        nutrition_advice.append("🥩 **Eat More Tryptophan-Rich Foods**: Turkey, eggs, and dairy contain tryptophan, an amino acid that boosts serotonin, helping regulate sleep patterns.")

    ## 🚶‍♂️ Low Activity (Few Steps Taken)
    if steps < 5000:
        nutrition_advice.append("🥩 **Increase Protein Intake**: Lean proteins (chicken, fish, tofu) help maintain muscle strength and support recovery after physical activity.")
        nutrition_advice.append("🍉 **Stay Hydrated**: Drinking enough water keeps your body energized and prevents fatigue, encouraging more movement.")
        nutrition_advice.append("🍠 **Eat More Complex Carbs**: Sweet potatoes, quinoa, and oats provide sustained energy, making it easier to stay active.")

    ## 🍽️ General Health Boosters
    nutrition_advice.append("🥗 **Eat a Rainbow**: A variety of colorful fruits and vegetables provide essential vitamins and antioxidants that strengthen the immune system.")
    nutrition_advice.append("💧 **Drink Plenty of Water**: Staying hydrated supports digestion, metabolism, and overall well-being.")
    nutrition_advice.append("🥚 **Include Probiotics in Your Diet**: Yogurt, kefir, and fermented foods improve gut health, which is linked to better immunity and digestion.")
    nutrition_advice.append("🥜 **Consume Iron-Rich Foods**: Spinach, lentils, and red meat help prevent fatigue and improve oxygen circulation in the body.")

    # Display nutrition suggestions
    if nutrition_advice:
        for advice in nutrition_advice:
            st.warning(advice)
    else:
        st.success("✅ Your nutrition and activity levels are optimal!")