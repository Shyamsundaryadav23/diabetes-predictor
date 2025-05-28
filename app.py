import streamlit as st
import joblib
import numpy as np

# Set page config
st.set_page_config(page_title="Diabetes Predictor", layout="centered", page_icon="🩺")

# Load the trained model
model = joblib.load("model.pkl")

# Sidebar
st.sidebar.title("About")
st.sidebar.info("""
This app predicts diabetes disease progression using 10 key medical features.
\nTrained using a regression model from the diabetes dataset.
""")

# Main Title
st.title("🩺 Diabetes Progression Predictor")
st.markdown("Enter patient features below to estimate future disease progression.")

# Input UI in columns
with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=0.0, max_value=100.0, value=50.0)
        sex = st.selectbox("Sex", options=[("Male", 1.0), ("Female", 0.0)], format_func=lambda x: x[0])[1]
        bmi = st.number_input("BMI", min_value=0.0, max_value=50.0, value=25.0)
        bp = st.number_input("Blood Pressure", min_value=0.0, max_value=150.0, value=75.0)
        s1 = st.number_input("S1", min_value=-100.0, max_value=300.0, value=100.0)

    with col2:
        s2 = st.number_input("S2", min_value=-100.0, max_value=300.0, value=100.0)
        s3 = st.number_input("S3", min_value=-100.0, max_value=300.0, value=100.0)
        s4 = st.number_input("S4", min_value=-100.0, max_value=300.0, value=100.0)
        s5 = st.number_input("S5", min_value=-100.0, max_value=300.0, value=100.0)
        s6 = st.number_input("S6", min_value=-100.0, max_value=300.0, value=100.0)

    submit = st.form_submit_button("Predict Progression")

# Prediction
if submit:
    try:
        features = [age, sex, bmi, bp, s1, s2, s3, s4, s5, s6]
        features = np.array(features).reshape(1, -1)
        prediction = model.predict(features)[0]

        st.markdown("---")
        st.success("🎯 Prediction Complete!")
        st.markdown(f"### 🧬 Predicted Disease Progression: `{prediction:.2f}`")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
