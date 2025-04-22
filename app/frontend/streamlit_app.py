import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Fraudulent Transaction Detection",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .custom-header {
        background: linear-gradient(to right, #2e8b57, #3cb371);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
    }
    @media (prefers-color-scheme: dark) {
        .custom-header {
            background: linear-gradient(to right, #14532d, #166534);
        }
    }
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
        font-size: 18px;
        gap: 2rem;
    }
    </style>

    <div class="custom-header">
        <h1 style="font-size: 3rem;">🔍 Fraudulent Transaction Detection</h1>
        <p style="font-size: 1.2rem;">Use Machine Learning or Gemini AI to evaluate a transaction's legitimacy.</p>
    </div>
""", unsafe_allow_html=True)

# API endpoint
API_BASE = "https://ml-model-for-fraud-detection-and-risk.onrender.com/api"

# Model selector
st.markdown("""
    <div style="text-align:center; font-size: 22px; margin-top: 20px;">
        🔧 <strong>Choose a Prediction Model</strong>
    </div>
""", unsafe_allow_html=True)

model_option = st.radio("", ["ML Model", "AI Model (Gemini)"], horizontal=True)

# Input fields
fields = {
    "Transaction_Amount": 1200.50,
    "Account_Balance": 5000.00,
    "IP_Address_Flag": 1,
    "Daily_Transaction_Count": 3,
    "Avg_Transaction_Amount_7d": 1100.00,
    "Failed_Transaction_Count_7d": 1,
    "Transaction_Distance": 20.5,
    "Risk_Score": 0.85,
    "Amount_to_Balance_Ratio": 0.24,
    "Amount_Deviation": 0.12,
    "Previous_Fraudulent_Activity": 0,
    "Is_Weekend": 0,
    "Hour": 12,
    "DayOfWeek": 3,
    "Is_Night": 0,
    "High_Risk_Category": 0
}

st.markdown("### 📝 Enter Transaction Details")

# 4-column layout
user_input = {}
cols = st.columns(4)
for idx, (key, default) in enumerate(fields.items()):
    with cols[idx % 4]:
        user_input[key] = st.number_input(key.replace("_", " "), value=float(default), format="%.2f")

# Submit Button
if st.button("🚀 Predict Transaction", use_container_width=True):
    endpoint = f"{API_BASE}/predict" if model_option == "ML Model" else f"{API_BASE}/ai-prediction"

    with st.spinner("⏳ Contacting server..."):
        try:
            response = requests.post(endpoint, json=user_input)
            result = response.json()
        except Exception as e:
            st.error("❌ Could not parse server response.")
            st.code(response.text)
            raise e

    st.markdown("---")
    st.subheader("📢 Prediction Result")

    # 🎯 Adaptive styling result display
    st.markdown("""
        <style>
        .result-box {
            padding: 20px;
            border-radius: 10px;
            margin-top: 10px;
        }
        .ml-box {
            background-color: #e6ffed;
            border-left: 8px solid #2e8b57;
        }
        .ai-box {
            background-color: #f0f8ff;
            border-left: 8px solid #1e90ff;
        }

        @media (prefers-color-scheme: dark) {
            .ml-box {
                background-color: #042f1a;
                border-left: 8px solid #00ff99;
                color: #e6ffe6;
            }
            .ai-box {
                background-color: #061d2b;
                border-left: 8px solid #3399ff;
                color: #e6f7ff;
            }
        }

        .explanation-box {
            background: #eaf4ff;
            padding: 15px;
            border-radius: 10px;
            white-space: pre-wrap;
            font-family: monospace;
        }

        @media (prefers-color-scheme: dark) {
            .explanation-box {
                background: #0b2a40;
                color: #d0e7ff;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Conditional content
    if response.status_code == 200:
        if model_option == "ML Model":
            prediction = result['label']
            probability = result['probability']
            st.markdown(f"""
                <div class="result-box ml-box">
                    <h2>🟢 Prediction: {prediction}</h2>
                    <p style="font-size:18px;">📊 <strong>Probability:</strong> {probability:.4f}</p>
                </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                <div class="result-box ai-box">
                    <h2>🧠 AI Model Prediction: {result['prediction']}</h2>
                    <p style="font-size:16px;"><strong>Explanation:</strong></p>
                    <div class="explanation-box">{result['explanation']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("❌ Prediction failed. Please check input or server.")
        st.code(result)