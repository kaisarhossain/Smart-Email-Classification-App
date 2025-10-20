import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv
import os
import random
import numpy as np
import pandas as pd
from huggingface_hub import login

# ----------------------------
# 1. Streamlit App Configuration
# ----------------------------
st.set_page_config(
    page_title="Email Classifier using NLP",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# 2. Custom Styling
# ----------------------------
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
            margin-bottom: 40px;
        }
        .email-list {
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            height: 500px;
            overflow-y: auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .email-item {
            padding: 10px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
        }
        .email-item:hover {
            background-color: #f5f5f5;
        }
        .email-content {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            height: 500px;
            overflow-y: auto;
        }
        .prediction-card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 3. App Header
# ----------------------------
st.markdown("<h1 class='main-title'>📧 Smart Email Classifier</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Smart Email Classification App is an advanced Natural Language Processing (NLP) and Deep Learning project designed to automate email intent classification. The application is capable of categorizing emails into six widely-used categories: Promotions, Spam, Social Media Updates, Forum Updates, Code Verification, and Work Updates.</p>", unsafe_allow_html=True)

# ----------------------------
# 4. Sidebar: Model Selection
# ----------------------------
st.sidebar.header("⚙️ Model Configuration")

# Define model options
model_options = {
    "DistilBERT (Fine-tuned) 1": "kaisarhossain/email-classifier-distilbert-finetuned-kaisar",
    "DistilBERT (Fine-tuned) 2": "kaisarhossain/email_classifier_model"
}

model_choice = st.sidebar.selectbox("Select Model", list(model_options.keys()))
MODEL_REPO = model_options[model_choice]
st.sidebar.info(f"Using model: {MODEL_REPO}")

# ----------------------------
# 5. Environment Variables & Authentication
# ----------------------------
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN:
    try:
        login(token=HF_TOKEN)
    except Exception as e:
        st.sidebar.warning("⚠️ Unable to authenticate with Hugging Face token.")
        st.sidebar.write(e)

# ----------------------------
# 6. Load Model Dynamically
# ----------------------------
@st.cache_resource(show_spinner=True)
def load_model(model_repo):
    tokenizer = AutoTokenizer.from_pretrained(model_repo)
    model = AutoModelForSequenceClassification.from_pretrained(model_repo)
    return tokenizer, model

try:
    tokenizer, model = load_model(MODEL_REPO)
except Exception as e:
    st.error(f"❌ Failed to load model from {MODEL_REPO}")
    st.exception(e)
    st.stop()

# ----------------------------
# 7. Labels and Dummy Inbox
# ----------------------------
LABELS = [
    "Promotions",
    "Spam",
    "Social Media Updates",
    "Forum Updates",
    "Code Verification",
    "Work Updates"
]

dummy_subjects = {
    "Promotions": ["50% OFF Today Only!", "Your Exclusive Coupon Awaits", "Flash Sale on Electronics"],
    "Spam": ["Claim your free reward!", "Win an iPhone 15 now!", "You’ve been selected!"],
    "Social Media Updates": ["New friend request on Facebook", "Someone mentioned you on Twitter", "New followers on Instagram"],
    "Forum Updates": ["Your Stack Overflow answer received upvotes", "New discussion thread in Data Science Forum", "Python 3.12 update discussion"],
    "Code Verification": ["Your verification code is 482915", "Confirm login attempt", "Verify your new device"],
    "Work Updates": ["Meeting rescheduled for 3 PM", "Project deadline extended", "Client feedback received"]
}

dummy_bodies = {
    "Promotions": "Get up to 70% off on your favorite brands. Offer valid for a limited time only!",
    "Spam": "Click this link to win cash prizes. Limited slots available!",
    "Social Media Updates": "You have new notifications and updates from your social media network.",
    "Forum Updates": "A new reply has been posted to a thread you are following.",
    "Code Verification": "Enter this code in the app to verify your login session.",
    "Work Updates": "Please find attached the meeting notes and next steps for the team."
}

# Generate dummy Gmail inbox
random.seed(42)
inbox_data = []
for _ in range(100):
    label = random.choice(LABELS)
    inbox_data.append({
        "Category": label,
        "Subject": random.choice(dummy_subjects[label]),
        "Body": dummy_bodies[label]
    })
inbox_df = pd.DataFrame(inbox_data)

# ----------------------------
# 8. Classification Function
# ----------------------------
def classify_email(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        predicted_idx = torch.argmax(probs, dim=1).item()
    confidence = probs[0][predicted_idx].item()
    return LABELS[predicted_idx], confidence, probs[0].numpy()

# ----------------------------
# 9. Gmail-like Layout
# ----------------------------
st.markdown("## 📥 Inbox")
st.markdown("---")
col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    st.markdown("#### 📩 Inbox")
    selected_email = st.radio(
        "Choose an email to view:",
        range(len(inbox_df)),
        format_func=lambda i: inbox_df.iloc[i]["Subject"],
        label_visibility="collapsed",
        index=None
    )

with col2:
    st.markdown("#### ✉️ Email Details")
    if selected_email is not None:
        selected_row = inbox_df.iloc[selected_email]
        st.markdown(f"**Subject:** {selected_row['Subject']}")
        st.markdown(f"**Body:** {selected_row['Body']}")
    else:
        st.info("📩 Select an email from the inbox to view details.")

with col3:
    st.markdown("#### 📊 Classification Result")
    if selected_email is not None:
        text = inbox_df.iloc[selected_email]["Subject"] + " " + inbox_df.iloc[selected_email]["Body"]
        predicted_label, confidence, all_probs = classify_email(text)
        st.markdown(f"**Predicted Category:** {predicted_label}")
        st.markdown(f"**Confidence:** {confidence * 100:.2f}%")
        prob_dict = {LABELS[i]: float(all_probs[i]) for i in range(len(LABELS))}
        st.bar_chart(prob_dict)
    else:
        st.warning("Select an email to see classification results.")

# ----------------------------
# 10. Manual Custom Email Input
# ----------------------------
st.markdown("---")
st.subheader("✉️ Enter email text (subject/body) for classification:")
email_text = st.text_area(
    "Enter Email Text Below:",
    placeholder="Example: Your code for verification is 123456 or Meeting scheduled for 3 PM today.",
    height=150
)

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

        prob_dict = {LABELS[i]: float(all_probs[i]) for i in range(len(LABELS))}
        st.markdown("#### 📊 Category Probabilities:")
        st.bar_chart(prob_dict)
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# 11. Footer
# ----------------------------
st.markdown("---")
st.markdown("""
    <p style='text-align: left; color: gray; font-size: 0.9rem'>
    Built for CSC-546: Natural Language Processing (Smart Email Classification Project) | 
    Developed by: Mohammed Golam Kaisar Hossain Bhuyan (hossainbhuyan@cua.edu)
    </p>
""", unsafe_allow_html=True)
