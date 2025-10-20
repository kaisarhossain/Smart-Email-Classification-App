import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv
import os
from huggingface_hub import login
import numpy as np

# 1. Streamlit App Configuration
st.set_page_config(
    page_title="Email Classifier using NLP",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #eef2f3, #8e9eab);
        }
        .main-title {
            text-align: center;
            color: #222;
            font-size: 2.3rem;
            font-weight: 700;
        }
        .sub-title {
            text-align: center;
            color: #444;
            font-size: 1.1rem;
        }
        .prediction-card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📧 Smart Email Classifier</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>The Smart Email Classifier application is capable of classifying emails of different types based on email subject or body using advanced Natural Language Processing (NLP) techniques and using a fine-tuned NLP model.</p>", unsafe_allow_html=True)


# 2. Load Environment Variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_REPO = os.getenv("MODEL_REPO", "kaisarhossain/email_classifier_model")  # default fallback

# Login to Hugging Face (optional if model is public)
if HF_TOKEN:
    login(token=HF_TOKEN)

# 3. Load Model & Tokenizer
@st.cache_resource(show_spinner=True)
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_REPO)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_REPO)
    return tokenizer, model

tokenizer, model = load_model()

# Define the label schema
LABELS = [
    "Promotions",
    "Spam",
    "Social Media Updates",
    "Forum Updates",
    "Code Verification",
    "Work Updates"
]

# 4. User Input Section
with st.container():
    st.subheader("✉️ Enter email text (subject/body) for classification:")
    email_text = st.text_area(
        "Enter Email Text Below:",
        placeholder="Example: Your code for verification is 123456 or Meeting scheduled for 3 PM today.",
        height=150
    )

# 5. Prediction Logic
def classify_email(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        predicted_idx = torch.argmax(probs, dim=1).item()
    confidence = probs[0][predicted_idx].item()
    return LABELS[predicted_idx], confidence, probs[0].numpy()

# 6. Predict Button
if st.button("🔍 Classify Email"):
    if not email_text.strip():
        st.warning("⚠️ Please enter email text before classifying.")
    else:
        with st.spinner("Classifying..."):
            predicted_label, confidence, all_probs = classify_email(email_text)

        st.markdown("<div class='prediction-card'>", unsafe_allow_html=True)
        st.markdown(f"### 🧠 Predicted Category: **{predicted_label}**")
        st.markdown(f"**Confidence:** {confidence * 100:.2f}%")
        st.progress(confidence)

        # Display class probabilities in a bar chart
        st.markdown("#### 📊 Category Probabilities:")
        prob_dict = {LABELS[i]: float(all_probs[i]) for i in range(len(LABELS))}
        st.bar_chart(prob_dict)
        st.markdown("</div>", unsafe_allow_html=True)

# 7. Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: left; color: gray; font-size: 0.9rem'>
    Built for CSC-546: Natural Language Processing (Smart Email Classification Project) | 
    Built by: Mohammed Golam Kaisar Hossain Bhuyan (hossainbhuyan@cua.edu)
    </p>

""", unsafe_allow_html=True)
